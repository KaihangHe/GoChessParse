import cv2
import numpy as np
import tensorflow as tf
from object_detection.utils import label_map_util


class SSDNet:
    def __init__(self, frozen_graph_path, pbtxt_path):
        self.__load_frozen_graph__(frozen_graph_path)
        self.__category_index__ = label_map_util.create_category_index_from_labelmap(pbtxt_path, use_display_name=True)
        self.__sess__ = self.__start_session__()

    def __load_frozen_graph__(self, frozen_graph_path):
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(frozen_graph_path, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

    def __start_session__(self):
        graph = self.detection_graph
        with graph.as_default():
            with tf.Session() as sess:
                return sess

    def __forward__(self, sess, image):
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
        output_dict = sess.run(tensor_dict, feed_dict={image_tensor: image})
