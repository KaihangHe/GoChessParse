import cv2
import numpy as np
from . import ssd_net

class ChessBoardParser:
    def __init__(self):
        pass

    def output(self,image):
        cv2.cvtColor(image,cv2.COLOR_BGR2RGB,image)
        center_lists=ssd_net.detect_chesspieces(image)
        for pt in center_lists:
            print(pt)
        output_matrix=[]
        return output_matrix

    def detect_chesspieces(self,image):
        ssd_net.__forward__(image)