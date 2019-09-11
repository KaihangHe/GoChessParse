import cv2
from .SSDNet import SSDNet
from .ChessBoardParser import ChessBoardParser
import json

ssd_net = SSDNet(frozen_graph_path='models/frozen_inference_graph.pb', pbtxt_path='models/go.pbtxt')

def output_result(image_Path,show_result):
    parser = ChessBoardParser()
    image = cv2.imread(image_Path)
    image = cv2.resize(image, (600, 600))
    try:
        center_lists = ssd_net.detect_chesspieces(InputArray=image)
    except ZeroDivisionError:
        print('ssd_net.detect_chesspieces ZeroDivisionError')
    if show_result:
        show_image = ChessBoardParser.draw_chesspieces_locate(image=image, center_lists=center_lists)
        cv2.imshow('show_image', show_image)
        cv2.waitKey()
    output_matrix = json.dumps(parser.output(image, center_lists).tolist())
    return output_matrix
