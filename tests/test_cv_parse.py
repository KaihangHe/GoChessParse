import cv2
import unittest
import numpy as np
from app.cv_parse.SSDNet import SSDNet


class CvTestCase(unittest.TestCase):
    def setUp(self):
        self.ssd_net = SSDNet(frozen_graph_path='models/frozen_inference_graph.pb', pbtxt_path='models/go.pbtxt')

    def tearDown(self):
        pass

    def test_have_load_graph(self):
        self.assertFalse(self.ssd_net.__sess__ == None)

    def test_forward(self):
        image = cv2.imread('static/srcImage.jpg')
        input_array = np.array([image, image, image, image])
        output = self.ssd_net.__forward__(input_array)
        self.assertFalse(output == None)
