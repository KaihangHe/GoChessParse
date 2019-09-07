import cv2
import numpy as np
from . import ssd_net

class ChessBoardParser:
    def __init__(self):
        pass

    def output(self,image):
        output_matrix=np.array([0])
        return output_matrix

    def detect_chesspieces(self,image):
        ssd_net.__forward__(image)