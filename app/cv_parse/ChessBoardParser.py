import cv2
import numpy as np

class ChessBoardParser:
    def __init__(self):
        pass

    def output(self, srcImage, center_list):
        maskImage = np.zeros((srcImage.shape[0], srcImage.shape[1]), np.uint8)
        edgeImage = self.__rebuildChessboard__(srcImage, center_list)
        edge_lines = self.__houghEdge__(edgeImage, srcImage)
        corners_list = []
        self.__get__pieces_mask(maskImage,center_list)
        for index in range(len(edge_lines)):
            corners_list.append(self.__clac_intersection(edge_lines[index], edge_lines[(index + 1) % 4]))
        dstImage, center_list = self.__remapLocate__(edgeImage, corners_list, maskImage, srcImage.shape[0:2])
        chess_board_pos = self.__shadowHist__(dstImage)
        chess_board_pos = self.__validate_edge_line__(chess_board_pos, dstImage, center_list)
        output_matrix = self.__position__(chess_board_pos, center_list)
        print('output_matrix shape\n', output_matrix.shape)
        return output_matrix

    @staticmethod
    def draw_chesspieces_locate(image, center_lists):
        show_image=image.copy()
        for center_info in center_lists:
            color = (0, 255, 0)
            if center_info[2] == 1:
                color = (255, 0, 0)
            cv2.rectangle(show_image, center_info[3], center_info[4], color, 2)
        return show_image


    def __get__pieces_mask(self,maskImage,center_list):
        for center in center_list:
            color = 70
            if center[2] == 2:
                color = 255
            cv2.circle(maskImage, (center[0], center[1]), 8, color, -1)

    def __clac_intersection(self, line_a, line_b):
        x1_a, y1_a, x2_a, y2_a = line_a
        x1_b, y1_b, x2_b, y2_b = line_b
        A_a = y2_a - y1_a
        B_a = x1_a - x2_a
        C_a = x2_a * y1_a - x1_a * y2_a
        A_b = y2_b - y1_b
        B_b = x1_b - x2_b
        C_b = x2_b * y1_b - x1_b * y2_b
        m = A_a * B_b - A_b * B_a
        output_x = (C_b * B_a - C_a * B_b) / m
        output_y = (C_a * A_b - C_b * A_a) / m
        return (int(output_x), int(output_y))

    def __detect__(self, srcImage):
        center_list = self.__net.chess_piece_mark(srcImage)
        return center_list

    def __rebuildChessboard__(self, srcImage, center_list, padding_val=8):
        InputArray = srcImage.copy()
        cv2.GaussianBlur(InputArray, (3, 3), 1, InputArray)
        edgeImage = cv2.Canny(InputArray, 20, 80)
        for pt in center_list:
            # clear bg
            cv2.rectangle(edgeImage, (pt[3][0] - padding_val, pt[3][1] - padding_val),
                          (pt[4][0] + padding_val, pt[4][1] + padding_val), (0, 0, 0), -1)
            cv2.line(edgeImage, ((pt[3][0] + pt[4][0]) // 2, pt[3][1] - padding_val),
                     ((pt[3][0] + pt[4][0]) // 2, pt[4][1] + padding_val),
                     (255, 255, 255), 2)
            cv2.line(edgeImage, (pt[3][0] - padding_val, (pt[3][1] + pt[4][1]) // 2),
                     (pt[4][0] + padding_val, (pt[3][1] + pt[4][1]) // 2),
                     (255, 255, 255), 2)
        return edgeImage

    def __validate_edge_line__(self, chess_board_pos, edgeImage, center_list):
        temp_way_num = min(len(chess_board_pos[0]), len(chess_board_pos[1]))
        perhaps_ways = [9, 13, 19]
        delta_ways = []
        edgeImage = cv2.dilate(edgeImage, cv2.getStructuringElement(0, (12, 12)))
        _, edgeImage = cv2.threshold(edgeImage, 125, 255, cv2.THRESH_BINARY_INV)
        contours, hier = cv2.findContours(edgeImage, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        con_inf = []
        for con in contours:
            x, y, w, h = cv2.boundingRect(con)
            con_center = (x + w // 2, y + h // 2)
            area = abs(cv2.contourArea(con))
            con_inf.append((con_center, area))
        for way in perhaps_ways:
            delta_ways.append(abs(way - temp_way_num))
        way_num = perhaps_ways[delta_ways.index(min(delta_ways))]
        x_pairs, y_pairs = [], []
        parser_image = np.zeros([600, 600, 3], np.uint8)
        parser_image[:, :, 0] = edgeImage.copy() * 0.85
        cv2.waitKey()
        for pos_index in range(len(chess_board_pos[0]) - way_num + 1):
            pos_list = chess_board_pos[0][pos_index:pos_index + way_num]
            y_pairs.append([pos_list[0], pos_list[-1]])
        for pos_index in range(len(chess_board_pos[1]) - way_num + 1):
            pos_list = chess_board_pos[1][pos_index:pos_index + way_num]
            x_pairs.append([pos_list[0], pos_list[-1]])
        roi_list = []
        for y_pair in y_pairs:
            for x_pair in x_pairs:
                pt1 = (x_pair[0], y_pair[0])
                pt2 = (x_pair[1], y_pair[1])
                roi_list.append((pt1, pt2))
        roi_contour_anyis = []
        for roi in roi_list:
            pt1, pt2 = roi[0], roi[1]
            con_num = 0
            for inf in con_inf:
                center = inf[0]
                if center[0] > pt1[0] and center[0] < pt2[0] and center[1] > pt1[1] and center[1] < pt2[1]:
                    con_num += 1
                    cv2.circle(parser_image, center, 3, (0, 255, 0), -1)
            cv2.rectangle(parser_image, pt1, pt2, (0, 255, 0), 1)
            # cv2.imshow('rac', parser_image)
            # cv2.waitKey()
            parser_image = np.zeros([600, 600, 3], np.uint8)
            parser_image[:, :, 0] = edgeImage.copy()
            print(con_num)
            roi_contour_anyis.append(con_num)
        if len(roi_contour_anyis) <= 0:
            return chess_board_pos
        roi_index = roi_contour_anyis.index(max(roi_contour_anyis))
        output_roi = roi_list[roi_index]
        print('x min =', output_roi[0][0])
        print('x max =', output_roi[1][0])
        print('y min =', output_roi[0][1])
        print('y max =', output_roi[1][1])
        chess_board_pos[1] = list(filter(lambda pos: True if pos >= output_roi[0][0] else False, chess_board_pos[1]))
        chess_board_pos[1] = list(filter(lambda pos: True if pos <= output_roi[1][0] else False, chess_board_pos[1]))
        chess_board_pos[0] = list(filter(lambda pos: True if pos >= output_roi[0][1] else False, chess_board_pos[0]))
        chess_board_pos[0] = list(filter(lambda pos: True if pos <= output_roi[1][1] else False, chess_board_pos[0]))
        # print(chess_board_pos)
        return chess_board_pos

    def __houghEdge__(self, edgeImage, srcImage=None):
        thresh_min = min(edgeImage.shape)
        lines = cv2.HoughLinesP(edgeImage, 1.2, np.pi / 180, 160, minLineLength=int(edgeImage.shape[0] * 0.7),
                                maxLineGap=int(thresh_min * 0.5))
        line_image = np.zeros(edgeImage.shape, np.uint8)
        if lines is None:
            return [[0, 1, 5, 21], [8, 1, 5, 3], [4, 12, 0, 8], [41, 11, 20, 15]]
        lines_h = filter(lambda line: True if abs(line[0][1] - line[0][3]) > edgeImage.shape[0] * 0.5 else False,
                         lines)
        lines_v = filter(lambda line: True if abs(line[0][0] - line[0][2]) > edgeImage.shape[1] * 0.5 else False, lines)
        lines_h = sorted(lines_h, key=lambda line: line[0][0])
        lines_v = sorted(lines_v, key=lambda line: line[0][1])
        mask = np.zeros([srcImage.shape[0], srcImage.shape[1], 3], np.uint8)
        for index, line in enumerate(lines):
            pt1, pt2 = (line[0][0], line[0][1]), (line[0][2], line[0][3])
            cv2.line(srcImage, pt1, pt2, (0, 0, 255), 2)
            # cv2.imshow('mask_hough', mask)
        if len(lines_h) < 5 or len(lines_v) < 5:
            return [[0, 1, 5, 21], [8, 1, 5, 3], [4, 12, 0, 8], [41, 11, 20, 15]]
        return [lines_h[0][0], lines_v[0][0], lines_h[-1][0], lines_v[-1][0]]

    def __remapLocate__(self, edgeImage, corner_list, maskImage, output_Imageshape=(600, 600)):
        prespect_mat, dstImage = self.__remapImage__(edgeImage, corner_list, output_Imageshape)
        maskImage = cv2.warpPerspective(maskImage, prespect_mat, output_Imageshape)
        output_center_list = []
        # cv2.imshow('maskImage', maskImage)
        contours, hier = cv2.findContours(maskImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for con in contours:
            x, y, w, h = cv2.boundingRect(con)
            pixel = maskImage[y + h // 2, x + w // 2]
            color = 2
            if pixel < 100 and pixel > 0:
                color = 1
            output_center_list.append(((x + w // 2, y + h // 2), color))
        # cv2.imshow("dstImage", dstImage)
        return dstImage, output_center_list

    def __shadowHist__(self, edgeImage):
        chess_board_pos = []
        x_list, y_list = np.zeros((edgeImage.shape[0], 1)), np.zeros((edgeImage.shape[0], 1))
        x_hist, y_hist = np.zeros(edgeImage.shape, np.uint8), np.zeros(edgeImage.shape, np.uint8)
        for index_y, y in enumerate(edgeImage):
            for index_x, x in enumerate(y):
                if x != 0:
                    y_list[index_x] += 1
        for index_y, y in enumerate(edgeImage):
            for index_x, x in enumerate(y):
                if x != 0:
                    x_list[index_y] += 1
        x_aver, y_aver = 0, 0
        for val in x_list:
            x_aver += val
        for val in y_list:
            y_aver += val
        x_aver, y_aver = x_aver / len(x_list), y_aver / len(y_list)
        for index, val in enumerate(y_list):
            if val > y_aver * 1.3:
                cv2.line(y_hist, (index, 0), (index, val), (255, 0, 0), 1)
        for index, val in enumerate(x_list):
            if val > x_aver * 1.3:
                cv2.line(x_hist, (0, index), (val, index), (255, 0, 0), 1)
        y_roi = y_hist[0:50, 0:x_hist.shape[1]]
        x_roi = x_hist[0:x_hist.shape[0], 0:50]
        cv2.dilate(x_roi, cv2.getStructuringElement(0, (1, 7)), x_roi)
        cv2.dilate(y_roi, cv2.getStructuringElement(0, (7, 1)), y_roi)
        hist_image = [x_hist, y_hist]
        chess_board_pos = []
        for image_index, hist in enumerate(hist_image):
            contours, hier = cv2.findContours(hist, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            line_pos = []
            index = image_index
            hist_val = 1 - image_index
            for con in contours:
                max_index, max_hist_val = 0, 0
                for pt in con:
                    pt = pt[0]
                    if pt[index] > max_hist_val:
                        max_hist_val = pt[index]
                        max_index = pt[hist_val]
                line_pos.append(max_index)
            chess_board_pos.append(line_pos)
        for l in chess_board_pos[0]:
            cv2.line(x_hist, (0, l), (1000, l), (255, 0, 0), 1)
        for l in chess_board_pos[1]:
            cv2.line(y_hist, (l, 0), (l, 1000), (255, 0, 0), 1)
        # cv2.imshow("yhist", y_hist)
        # cv2.imshow("x_hist", x_hist)
        chess_board_pos[0].reverse()
        chess_board_pos[1].reverse()
        return chess_board_pos

    def __remapImage__(self,InputArray, corners, output_size):
        if (len(corners) != 4):
            print("corner num err")
        src_Mat = []
        dst_Mat = np.float32(
            [[0, 0],
             [output_size[0], 0],
             [output_size[0], output_size[1]],
             [0, output_size[1]]])
        for i, pt in enumerate(corners):
            src_Mat.append(list(pt))
        src_Mat = np.float32(src_Mat)
        perspective_mat = cv2.getPerspectiveTransform(src_Mat, dst_Mat)
        dstImage = cv2.warpPerspective(InputArray, perspective_mat, output_size)
        # cv2.imshow("dstImage", dstImage)
        # cv2.imwrite("dstImage7.jpg", dstImage)
        return perspective_mat, dstImage

    def __position__(self, chess_board_pos, center_list):
        parser_image = np.zeros([600, 600, 3], np.uint8)
        radius = abs(chess_board_pos[0][0] - chess_board_pos[0][-1]) // len(chess_board_pos[0])
        print("raduis", radius)
        radius *= 0.7
        output_mat = np.zeros([len(chess_board_pos[0]), len(chess_board_pos[1])], np.int)
        chess_position = []
        for index, y_val in enumerate(chess_board_pos[0]):
            chess_position.append([])
            for x_val in chess_board_pos[1]:
                chess_position[index].append((x_val, y_val))
        for center in center_list:
            color = center[1]
            center = (center[0])
            cv2.circle(parser_image, center, 5, (255 * (color - 1), 255, 0), -1)

        for index_y, chess_line in enumerate(chess_position):
            for index_x, pos in enumerate(chess_line):
                cv2.circle(parser_image, pos, 2, (255, 255, 255), -1)
                cv2.putText(parser_image, str(index_x) + ' , ' + str(index_y), (pos[0] - 5, pos[1] - 5), 1, 0.5,
                            (255, 0, 0), 1)

                x1, y1, x2, y2 = pos[0] - radius, pos[1] - radius, pos[0] + radius, pos[1] + radius
                for center in center_list:
                    color = center[1]
                    center = center[0]
                    if center[0] > x1 and center[0] < x2 and center[1] > y1 and center[1] < y2:
                        output_mat[index_y, index_x] = color
        # cv2.imshow('par',parser_image)
        # cv2.waitKey()
        return output_mat
