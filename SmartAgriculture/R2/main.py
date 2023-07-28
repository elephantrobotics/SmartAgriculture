from CvDetection.detection import Detector
from R2Control.Common import *
from R2Control.TcpServer import TcpServer
from R2Control.RobotR2 import RobotR2
from R2Control.VideoCapture3d import VideoCaptureThread
import time
import threading
# def start_server():
    

if __name__ == "__main__":
    server_address = ('127.0.0.1', 12345)
    server = TcpServer(server_address)
    server.start()
    # server = None
    r2 = RobotR2(
        server,
        'com19'
    )

    capture_thread = VideoCaptureThread(Detector("orange"), Detector.FetchType.FETCH.value)  # 创建3D摄像头线程
    capture_thread.daemon = True  # 设置守护线程
    capture_thread.start()  # 启动线程

    try:
        while True:
            camera_coord_list = capture_thread.get_camera_coord_list()
            fruit_type = capture_thread.get_fruit_type()
            r2.motion(camera_coord_list, fruit_type)
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    # 等待3D摄像头线程服务结束
    capture_thread.join()
    server.join()
