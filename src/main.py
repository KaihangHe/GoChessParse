import cv2
from src.WebInterface import *
from src.ChessBoardParse import *
if __name__ == '__main__':
    parser = ChessBoardParse('models/frozen_inference_graph.pb', 'models/go.pbtxt')
    parser.output_matrix('upload/1.jpg')
    cv2.waitKey()
    #  app.run(host='0.0.0.0', port='8080', debug=True)
