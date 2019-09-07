from .SSDNet import SSDNet

ssd_net = SSDNet(frozen_graph_path='models/frozen_inference_graph.pb', pbtxt_path='models/go.pbtxt')
