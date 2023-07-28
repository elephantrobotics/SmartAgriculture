from R1.R1Control.Common import *
from R1.CvDetection.detection import Detector
from R1.R1Control.TcpClient import TcpClient
from R1.R1Control.RobotR1 import RobotR1
from R1.R1Control.VideoCapture3d import VideoCaptureThread
import time
import numpy as np

client = None
class R1_run():
    def __init__(self,R1_port,conveyor_port):
        super(R1_run,self).__init__()
        self.client = TcpClient('127.0.0.1', 12345)
        self.client.response_copy = bad_fruit_str
        self.client.start()
        self.R1_port = R1_port
        self.Conveyor_port = conveyor_port
        self.capture_thread = None
        self.pixel_coord = np.array([0.0, 0.0, 0.0])
        self.real_coord = np.array([0.0, 0.0, 0.0])
        self.r1 = None

    def run(self):

        self.r1 = RobotR1(
            self.client,
            self.R1_port,
            self.Conveyor_port
        )
        self.capture_thread = VideoCaptureThread(Detector("apple"), Detector.FetchType.FETCH.value)
        self.capture_thread.daemon = True
        self.capture_thread.start()

        try:
            while True:
                self.r1.motion(self.capture_thread)
                time.sleep(1)
        except KeyboardInterrupt:
            pass

        self.capture_thread.join()



        # 关闭TCP客户端连接
        self.client.join()

    # def get_color(self):
    #     return self.capture_thread.rgb_show
    #
    # def get_depth(self):
    #     return self.capture_thread.depth_show

# if __name__ == "__main__":
#     client = TcpClient('127.0.0.1', 12345)
#     client.response_copy = bad_fruit_str
#     client.start()
#
#     r1 = RobotR1(
#         client,
#         'com9',
#         'com14'
#     )
#
#     capture_thread = VideoCaptureThread(Detector("apple"), Detector.FetchType.FETCH.value)
#     capture_thread.daemon = True
#     capture_thread.start()
#
#     try:
#         while True:
#             r1.motion(capture_thread)
#             time.sleep(1)
#     except KeyboardInterrupt:
#         pass
#
#     capture_thread.join()
#
#     # 关闭TCP客户端连接
#     client.join()