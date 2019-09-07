import cv2
import numpy as np
from . import ssd_net

class ChessBoardParser:
    def __init__(self):
        pass

    def output(self,image):
        pass

    def detect_chesspieces(self,image):
        ssd_net.__forward__(image)