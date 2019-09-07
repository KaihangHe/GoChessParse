import cv2
import numpy as np
import tensorflow as tf
from object_detection.utils import label_map_util


class SSDNet:
    def __init__(self, frozen_graph_path, pbtxt_path):
        '''

        :param frozen_graph_path:
        :param pbtxt_path:
        '''
        self.__load_frozen_graph__(frozen_graph_path)
        self.__sess__, self.tensor_dict, self.image_tensor = self.__load_tensor__()
        self.__category_index__ = label_map_util.create_category_index_from_labelmap(pbtxt_path, use_display_name=True)

    def __load_frozen_graph__(self, frozen_graph_path):
        '''

        :param frozen_graph_path:
        :return:
        '''
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(frozen_graph_path, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

    def __load_tensor__(self):
        '''

        :return:
        '''
        graph = self.detection_graph
        with graph.as_default():
            sess = tf.Session()
            ops = tf.get_default_graph().get_operations()
            all_tensor_names = {output.name for op in ops for output in op.outputs}
            tensor_dict = {}
            for key in [
                'num_detections', 'detection_boxes', 'detection_scores',
                'detection_classes', 'detection_masks'
            ]:
                tensor_name = key + ':0'
                if tensor_name in all_tensor_names:
                    tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
                        tensor_name)
            if 'detection_masks' in tensor_dict:
                detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
                detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
                real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
                detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
            image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')
            return sess, tensor_dict, image_tensor

    def __forward__(self, image):
        '''
        :param image:
        :return:
        '''
        return self.__sess__.run(self.tensor_dict, feed_dict={self.image_tensor: image})

    def __split_image__(self, InputArray):
        '''
        :param InputArray:
        :return:
        '''
        roi_list = []
        srcImage = InputArray.copy()
        width, height = srcImage.shape[1], srcImage.shape[0]
        roi_width, roi_height = int(width * 0.6), int(height * 0.6)
        cv2.cvtColor(srcImage, cv2.COLOR_BGR2RGB, srcImage)
        for y in range(2):
            for x in range(2):
                roi_tlx, roi_tly = int(width * 0.4) * x, int(height * 0.4) * y
                ROI = srcImage[roi_tly:roi_tly + roi_height, roi_tlx:roi_tlx + roi_width]
                roi_list.append(ROI)
        roi_input = np.array([roi_list[0], roi_list[1], roi_list[2], roi_list[3]])
        return roi_input

    def __concat_image_output__(self, output_dict, image_shape, split_ROI_shape):
        center_list = []
        index = 0
        aver = 0
        width, height = image_shape[1], image_shape[0]
        for y in range(2):
            for x in range(2):
                roi_tlx, roi_tly = int(width * 0.4) * x, int(height * 0.4) * y
                divide_x, divide_y = width // 2, height // 2
                output_roi = {}
                output_roi['num_detections'] = int(output_dict['num_detections'][index])
                output_roi['detection_classes'] = output_dict[
                    'detection_classes'][index].astype(np.uint8)
                output_roi['detection_boxes'] = output_dict['detection_boxes'][index]
                output_roi['detection_scores'] = output_dict['detection_scores'][index]
                index += 1
                center_temp = self.__get_chess_pieces_position__(split_ROI_shape, output_roi, 0.1)
                for p in center_temp:
                    p = (int(p[0] + roi_tlx), int(p[1] + roi_tly), int(p[2]), (p[3][0] + roi_tlx, p[3][1] + roi_tly),
                         (p[4][0] + roi_tlx, p[4][1] + roi_tly))
                    if x == 0 and y == 0 and (p[0] > divide_x or p[1] > divide_y):
                        continue
                    elif x == 1 and y == 0 and (p[0] < divide_x or p[1] > divide_y):
                        continue
                    elif x == 0 and y == 1 and (p[0] > divide_x or p[1] < divide_y):
                        continue
                    elif x == 1 and y == 1 and (p[0] < divide_x or p[1] < divide_y):
                        continue
                    center_list.append(p)
                    aver += (abs(p[3][0] - p[4][0]) + abs(p[3][1] - p[4][1])) // 2
        aver /= len(center_list)
        # print('aver=', aver)
        for index, temp in enumerate(center_list):
            size_val = (abs(temp[3][0] - temp[4][0]) + abs(temp[3][1] - temp[4][1])) // 2
            if size_val < aver * 0.7:
                center_list.pop(index)
        return center_list

    def detect_chesspieces(self, InputArray):
        '''
        :param InputArray:
        :return:
        '''
        center_list = []
        roi_input = self.__split_image__(InputArray)
        output = self.__forward__(roi_input)
        center_list = self.__concat_image_output__(output, InputArray.shape, roi_input[0].shape)
        # print('size_val=', size_val)
        # self.draw_pts(InputArray.copy(), center_list)
        return center_list

    def __get_chess_pieces_position__(self, InputImage_shape, forward_result, beshowed_threshold=0.1):
        '''

        :param InputImage_shape:
        :param forward_result:
        :param beshowed_threshold:
        :return:
        '''
        h, w = InputImage_shape[0], InputImage_shape[1]
        chess_pieces_num = 0
        center_list = []
        for index, result in enumerate(forward_result['detection_scores']):
            if result < beshowed_threshold:
                break
            rect = forward_result['detection_boxes'][index]
            class_name = self.__category_index__[forward_result['detection_classes'][index]]
            pt1 = ((int)(rect[1] * w), (int)(rect[0] * h))
            pt2 = ((int)(rect[3] * w), (int)(rect[2] * h))
            center = (
                (pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2, forward_result['detection_classes'][index], pt1, pt2)
            center_list.append(center)
            chess_pieces_num += 1
        return center_list
