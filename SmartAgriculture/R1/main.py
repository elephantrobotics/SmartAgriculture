from R1Control.Common import *
from CvDetection.detection import Detector
from R1Control.TcpClient import TcpClient
from R1Control.RobotR1 import RobotR1
from R1Control.VideoCapture3d import VideoCaptureThread
import time

client = None

if __name__ == "__main__":
    client = TcpClient('127.0.0.1', 12345)
    client.response_copy = bad_fruit_str
    client.start()

    r1 = RobotR1(
        client,
        'com9',
        'com14'
    )

    capture_thread = VideoCaptureThread(Detector("apple"), Detector.FetchType.FETCH.value)
    capture_thread.daemon = True
    capture_thread.start()

    try:
        while True:
            r1.motion(capture_thread)
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    capture_thread.join()

    # 关闭TCP客户端连接
    client.join()