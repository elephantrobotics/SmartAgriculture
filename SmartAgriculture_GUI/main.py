import logging
import os
import sys
import threading
import time
import traceback

import numpy as np
import serial
import serial.tools.list_ports
from PyQt5.Qt import *

from R1.ConveyorControl.ConveyorMain import ConveyorMain
from R1.main import R1_run
from R2.main import R2_run
# from lib.ui_SmartAgriculture import Ui_MainWindow as SmartKit_window
from lib.ui_SmartAgriculture_opt import Ui_MainWindow as SmartKit_window

protocol_handler_packages = [
    'serial.urlhandler',
]


class MyLogging:
    def __init__(self):
        timestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        lib_path = os.path.split(os.path.abspath(__file__))
        filename = './error.log'  # 日志文件的地址
        # print(filename)
        self.logger = logging.getLogger()  # 定义对应的程序模块名name，默认为root
        self.logger.setLevel(logging.DEBUG)  # 必须设置，这里如果不显示设置，默认过滤掉warning之前的所有级别的信息
        # 设置格式对象
        formatter = logging.Formatter(
            "%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s - %(message)s")  # 定义日志输出格式

        sh = logging.StreamHandler()  # 日志输出到屏幕控制台
        sh.setLevel(logging.INFO)  # 设置日志等级
        sh.setFormatter(formatter)  # 设置handler的格式对象

        fh = logging.FileHandler(filename=filename, encoding='utf-8')  # 向文件filename输出日志信息
        fh.setLevel(logging.INFO)  # 设置日志等级
        fh.setFormatter(formatter)  # 设置handler的格式对象

        # 将handler增加到logger中
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)


class SmartKit_APP(SmartKit_window, QMainWindow, QWidget):
    def __init__(self):
        super(SmartKit_APP, self).__init__()
        self.setupUi(self)
        self.comboBox_R1port.highlighted.connect(self.get_serial_port_list)
        self.comboBox_R1port.activated.connect(self.get_serial_port_list)
        self.comboBox_R2port.highlighted.connect(self.get_serial_port_list)
        self.comboBox_R2port.activated.connect(self.get_serial_port_list)
        self.comboBox_ConveyorPort.highlighted.connect(self.get_serial_port_list)
        self.comboBox_ConveyorPort.activated.connect(self.get_serial_port_list)
        self.pushButton_ConveyorConnect.clicked.connect(self.conveyor_check)

        self.port_list = []
        self.get_serial_port_list()
        self.camera1_mode = 0
        self.camera2_mode = 0
        self.r1 = None
        self.r2 = None
        self.conveyor = None
        self.r1_move = False
        self.r2_move = False
        self.language_mode = None
        self.language_mode = self.comboBox_language.currentText()

        self.pushButton_showPixelCoords.clicked.connect(self.get_pixel_coords)
        self.pushButton_showRealCoords.clicked.connect(self.get_real_coords)

        self.pushButton_R1Connect.clicked.connect(self.check1)
        self.pushButton_R2Connect.clicked.connect(self.check2)

        self.pushButton_openCamera1.clicked.connect(self.camera1_check)
        self.pushButton_openCamera2.clicked.connect(self.camera2_check)

        self.pushButton_ConveyorOpen.clicked.connect(self.open_conveyor)
        self.pushButton_ConveyorClose.clicked.connect(self.close_conveyor)

        self.pushButton_language.clicked.connect(self.change_language)

        self.pushButton_R1run.clicked.connect(self.run_R1)
        self.pushButton_R2run.clicked.connect(self.run_R2)

        self.label_logo.setPixmap(QPixmap("./lib/logo.png"))
        self.init_btn_status()  # 初始化按钮状态颜色
        self.R1_run_status = False  # 是否运行采摘机器人R1
        self.R2_run_status = False  # 是否运行分拣机器人R2
        self.ConveyorOpen_status = False  # 是否打开传送带
        self.ConveyorClose_status = False  # 是否关闭传送带
        self.openCamera1_status = False  # 是否打开果树3D相机
        self.openCamera2_status = False  # 是否打开传送带3D相机
        # 日志信息
        self.loger = MyLogging().logger

    def btn_color(self, btn, color):
        """
        设置按钮颜色
        """
        if color == 'red':
            btn.setStyleSheet("background-color: rgb(231, 76, 60);\n"
                              "color: rgb(255, 255, 255);\n"
                              "border-radius: 10px;\n"
                              "border: 2px groove gray;\n"
                              "border-style: outset;")
        elif color == 'green':
            btn.setStyleSheet("background-color: rgb(39, 174, 96);\n"
                              "color: rgb(255, 255, 255);\n"
                              "border-radius: 10px;\n"
                              "border: 2px groove gray;\n"
                              "border-style: outset;")
        elif color == 'blue':
            btn.setStyleSheet("background-color: rgb(41, 128, 185);\n"
                              "color: rgb(255, 255, 255);\n"
                              "border-radius: 10px;\n"
                              "border: 2px groove gray;\n"
                              "border-style: outset;")
        elif color == 'gray':
            btn.setStyleSheet("background-color: rgb(185, 195, 199);\n"
                              "color: rgb(255, 255, 255);\n"
                              "border-radius: 10px;\n"
                              "border: 2px groove gray;\n"
                              "border-style: outset;")

    def init_btn_status(self):
        """
        初始化各个按钮的状态
        """
        btn_list = [self.pushButton_R1run, self.pushButton_R2run, self.pushButton_ConveyorOpen,
                    self.pushButton_ConveyorClose, self.pushButton_openCamera1, self.pushButton_openCamera2,
                    self.pushButton_showRealCoords, self.pushButton_showPixelCoords]
        for b in btn_list:
            b.setEnabled(False)
            self.btn_color(b, 'gray')

    def change_language(self):
        """
        语言切换线程
        """
        try:
            language = threading.Thread(target=self.language_change)
            language.start()
        except KeyboardInterrupt:
            pass

    def language_change(self):
        self.language_mode = self.comboBox_language.currentText()
        if self.language_mode == "中文":
            self.btn_color(self.pushButton_language, 'green')
            self.lineEdit_13.setText("采摘机器人")
            self.lineEdit_17.setText("设备")
            self.lineEdit_16.setText("串口")
            self.lineEdit_18.setText("波特率")
            self.pushButton_R1Connect.setText("连接")
            self.pushButton_R1run.setText("运行")
            self.pushButton_language.setText("保存")

            self.lineEdit_7.setText("分拣机器人")
            self.lineEdit_9.setText("设备")
            self.lineEdit_8.setText("串口")
            self.lineEdit_10.setText("波特率")
            self.pushButton_R2Connect.setText("连接")
            self.pushButton_R2run.setText("运行")

            self.lineEdit_19.setText("传送带")
            self.lineEdit_20.setText("串口")
            self.pushButton_ConveyorConnect.setText("连接")
            self.pushButton_ConveyorOpen.setText("打开")
            self.pushButton_ConveyorClose.setText("关闭")

            self.lineEdit_24.setText("果树3D相机画面")
            self.lineEdit_25.setText("传送带3D相机画面")
            self.pushButton_openCamera1.setText("打开")
            self.pushButton_openCamera2.setText("打开")

            self.lineEdit_23.setText("坐标显示")
            self.pushButton_showRealCoords.setText("果子坐标（相对于机械臂）")
            self.pushButton_showPixelCoords.setText("果子坐标（相对于相机）")
        elif self.language_mode == "English":
            self.btn_color(self.pushButton_language, 'blue')
            self.lineEdit_13.setText(" Harvesting Robotics")
            self.lineEdit_17.setText("Model")
            self.lineEdit_16.setText("Serial Port")
            self.lineEdit_18.setText("Baud")
            self.pushButton_R1Connect.setText("Connect")
            self.pushButton_R1run.setText("Run")
            self.pushButton_language.setText("Save")

            self.lineEdit_7.setText("Sorting Robotics")
            self.lineEdit_9.setText("Model")
            self.lineEdit_8.setText("Serial Port")
            self.lineEdit_10.setText("Baud")
            self.pushButton_R2Connect.setText("Connect")
            self.pushButton_R2run.setText("Run")

            self.lineEdit_19.setText("Conveyor Belt")
            self.lineEdit_20.setText("Serial Port")
            self.pushButton_ConveyorConnect.setText("Connect")
            self.pushButton_ConveyorOpen.setText("Open")
            self.pushButton_ConveyorClose.setText("Close")

            self.lineEdit_24.setText("3D Camera Footage of Fruit Trees")
            self.lineEdit_25.setText("3D Camera Footage of Conveyor Belt")
            self.pushButton_openCamera1.setText("Open")
            self.pushButton_openCamera2.setText("Open")

            self.lineEdit_23.setText("Coordinates Display")
            self.pushButton_showRealCoords.setText("Fruit's coordinates (relative to robot)")
            self.pushButton_showPixelCoords.setText("Fruit's coordinates (relative to camera)")

    def get_pixel_coords(self):
        """
        获取果子相对于相机的坐标
        """
        try:
            get_coord = threading.Thread(target=self.get_pixel)
            get_coord.start()
        except Exception as e:
            self.loger.error(e)

    def get_pixel(self):
        while True:
            coord = [np.round(x, 2) for x in self.r1.r1.camera_coord]
            self.label_pixelcoords.setText("    X:" + str(coord[0]) + "   Y:" + str(coord[1]) + "   Z:" + str(coord[2]))
            time.sleep(0.5)

    # 获取果子相对于机械臂的坐标
    def get_real_coords(self):
        try:
            get_coord = threading.Thread(target=self.get_real)
            get_coord.start()
        except Exception as e:
            e = traceback.format_exc()
            self.loger.error(e)

    def get_real(self):
        while True:
            coord = [np.round(x, 2) for x in self.r1.r1.end_coords[:3]]
            self.label_realcoords.setText("    X:" + str(coord[0]) + "   Y:" + str(coord[1]) + "   Z:" + str(coord[2]))
            time.sleep(0.5)

    # 连接机械臂
    def check1(self):
        current_mode = self.pushButton_R1Connect.text()
        if current_mode == '连接' or current_mode == 'Connect':
            self.init_R1()
        elif current_mode == '断开' or current_mode == "Disconnect":
            self.disconnect_R1()

    def check2(self):
        current_mode = self.pushButton_R2Connect.text()
        if current_mode == '连接' or current_mode == 'Connect':
            self.init_R2()
        elif current_mode == '断开' or current_mode == "Disconnect":
            self.disconnect_R2()

    def conveyor_check(self):
        current_mode = self.pushButton_ConveyorConnect.text()
        if current_mode == '连接' or current_mode == "Connect":
            self.conveyor_connect()
        elif current_mode == '断开' or current_mode == "Disconnect":
            self.conveyor_disconnect()

    def showMessageBox(self):
        """
        机械臂连接失败弹框
        """
        # 创建 QMessageBox 对象
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Icon.Information)
        if self.language_mode == '中文':
            msgBox.setWindowTitle('提示')
            msgBox.setText('连接失败!请检查串口是否正确，是否被占用')
        elif self.language_mode == 'English':
            msgBox.setWindowTitle('Hint')
            msgBox.setText(
                'The connection failed, please check whether the serial port is correct and whether it is occupied')
        # msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.setStyleSheet("QMessageBox { background-color: rgb(185, 195, 199); }"
                             "QLabel { font-size: 18px; font-family: Arial; }")
        msgBox.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        msgBox.exec()

    def showMessageBox_camera(self):
        """
        相机打开失败弹窗
        """
        # 创建 QMessageBox 对象
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Icon.Information)
        if self.language_mode == '中文':
            msgBox.setWindowTitle('提示')
            msgBox.setText('相机打开失败，请检查摄像头是否正确连接.')
        elif self.language_mode == 'English':
            msgBox.setWindowTitle('Hint')
            msgBox.setText(
                'Failed to open the camera, please check whether the camera is connected correctly')
        # msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.setStyleSheet("QMessageBox { background-color: rgb(185, 195, 199); }"
                             "QLabel { font-size: 18px; font-family: Arial; }")
        msgBox.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        msgBox.exec()

    def init_R1(self):
        self.comboBox_R1device.setEnabled(False)
        self.comboBox_R1port.setEnabled(False)
        self.comboBox_R1baud.setEnabled(False)

        try:
            R1_port = self.comboBox_R1port.currentText()
            Conveyor_port = self.comboBox_ConveyorPort.currentText()
            self.r1 = R1_run(R1_port, Conveyor_port)
            self.r1_move = True
            self.loger.info('Connection Successful')
            self.pushButton_R1run.setEnabled(True)
            self.btn_color(self.pushButton_R1run, 'blue')
            self.pushButton_showRealCoords.setEnabled(True)
            self.pushButton_showPixelCoords.setEnabled(True)
            self.btn_color(self.pushButton_showPixelCoords, 'blue')
            self.btn_color(self.pushButton_showRealCoords, 'blue')
            if self.language_mode == '中文':
                self.pushButton_R1Connect.setText("断开")
            elif self.language_mode == 'English':
                self.pushButton_R1Connect.setText("Disconnect")
            self.btn_color(self.pushButton_R1Connect, 'red')

        except Exception as e:
            # print(e)
            e = traceback.format_exc()
            error_log = """Connection failed !!! :{}""".format(e)
            self.showMessageBox()
            self.comboBox_R1device.setEnabled(True)
            self.comboBox_R1port.setEnabled(True)
            self.comboBox_R1baud.setEnabled(True)
            self.pushButton_R1run.setEnabled(False)
            self.btn_color(self.pushButton_R1run, 'gray')
            self.pushButton_showRealCoords.setEnabled(False)
            self.pushButton_showPixelCoords.setEnabled(False)
            self.btn_color(self.pushButton_showPixelCoords, 'gray')
            self.btn_color(self.pushButton_showRealCoords, 'gray')
            if self.language_mode == '中文':
                self.pushButton_R1Connect.setText('连接')
                self.pushButton_R1run.setText('运行')
            elif self.language_mode == 'English':
                self.pushButton_R1Connect.setText('Connect')
                self.pushButton_R1run.setText('Run')
            self.btn_color(self.pushButton_R1Connect, 'green')
            self.loger.error(error_log)

    def init_R2(self):
        self.comboBox_R2device.setEnabled(False)
        self.comboBox_R2port.setEnabled(False)
        self.comboBox_R2baud.setEnabled(False)

        try:
            R2_port = self.comboBox_R2port.currentText()
            self.r2 = R2_run(R2_port)
            self.r2_move = True
            self.loger.info('Connection Successful')
            self.pushButton_R2run.setEnabled(True)
            self.btn_color(self.pushButton_R2run, 'blue')
            if self.conveyor is not None:
                self.conveyor = None
                self.pushButton_ConveyorOpen.setEnabled(False)
                self.pushButton_ConveyorClose.setEnabled(False)
                self.btn_color(self.pushButton_ConveyorOpen, 'gray')
                self.btn_color(self.pushButton_ConveyorClose, 'gray')
            if self.language_mode == '中文':
                self.pushButton_R2Connect.setText("断开")
                self.pushButton_ConveyorConnect.setText('连接')
            elif self.language_mode == 'English':
                self.pushButton_R2Connect.setText("Disconnect")
                self.pushButton_ConveyorConnect.setText('Connect')
            self.btn_color(self.pushButton_R2Connect, 'red')
            self.btn_color(self.pushButton_ConveyorConnect, 'green')

        except Exception as e:
            e = traceback.format_exc()
            self.showMessageBox()
            self.comboBox_R2device.setEnabled(True)
            self.comboBox_R2port.setEnabled(True)
            self.comboBox_R2baud.setEnabled(True)

            self.pushButton_R2run.setEnabled(False)
            self.btn_color(self.pushButton_R2run, 'gray')
            if self.language_mode == '中文':
                self.pushButton_R2Connect.setText('连接')
                self.pushButton_R2run.setText('运行')
            elif self.language_mode == 'English':
                self.pushButton_R2Connect.setText('Connect')
                self.pushButton_R2run.setText('Run')
            self.btn_color(self.pushButton_R2Connect, 'green')
            self.loger.error(e)

    # 程序启动
    def run_R1(self):
        self.pushButton_openCamera1.setEnabled(True)
        self.btn_color(self.pushButton_openCamera1, 'blue')
        if self.language_mode == '中文':
            self.pushButton_R1run.setText('运行中')
            self.btn_color(self.pushButton_R1run, 'red')
        else:
            self.pushButton_R1run.setText('running')
            self.btn_color(self.pushButton_R1run, 'red')
        self.pushButton_R1run.setEnabled(False)
        if self.r1_move:
            move = threading.Thread(target=self.r1.run)
            move.start()

    def run_R2(self):
        self.pushButton_openCamera2.setEnabled(True)
        self.btn_color(self.pushButton_openCamera2, 'blue')
        if self.language_mode == '中文':
            self.pushButton_R2run.setText('运行中')
            self.btn_color(self.pushButton_R2run, 'red')
        else:
            self.pushButton_R2run.setText('running')
            self.btn_color(self.pushButton_R2run, 'red')
        self.pushButton_R2run.setEnabled(False)
        if self.r2_move:
            move = threading.Thread(target=self.r2.run)
            move.start()

    def disconnect_R1(self):
        self.comboBox_R1device.setEnabled(True)
        self.comboBox_R1port.setEnabled(True)
        self.comboBox_R1baud.setEnabled(True)
        self.label_camera1_color.close()
        self.label_camera1_depth.close()
        self.r1.client = None
        self.conveyor = None
        self.r1.capture_thread = None
        self.r1 = None
        self.loger.info('Disconnection Successful')
        self.pushButton_openCamera1.setEnabled(False)
        self.btn_color(self.pushButton_openCamera1, 'gray')
        self.pushButton_showRealCoords.setEnabled(False)
        self.btn_color(self.pushButton_showRealCoords, 'gray')
        self.pushButton_showPixelCoords.setEnabled(False)
        self.btn_color(self.pushButton_showPixelCoords, 'gray')
        if self.language_mode == '中文':
            self.pushButton_R1Connect.setText("连接")
            self.pushButton_R1run.setText('运行')
        elif self.language_mode == 'English':
            self.pushButton_R1Connect.setText("Connect")
            self.pushButton_R1run.setText('Run')
        self.btn_color(self.pushButton_R1Connect, 'green')
        self.pushButton_R1run.setEnabled(False)
        self.btn_color(self.pushButton_R1run, 'gray')

    def disconnect_R2(self):
        self.comboBox_R2device.setEnabled(True)
        self.comboBox_R2port.setEnabled(True)
        self.comboBox_R2baud.setEnabled(True)
        self.label_camera2_color.close()
        self.label_camera2_depth.close()
        self.r2.server = None
        self.r2.capture_thread = None
        self.r2 = None
        self.loger.info('Disconnection Successful')
        self.pushButton_openCamera2.setEnabled(False)
        self.btn_color(self.pushButton_openCamera2, 'gray')
        if self.language_mode == '中文':
            self.pushButton_R2Connect.setText("连接")
            self.pushButton_R2run.setText('运行')
        elif self.language_mode == 'English':
            self.pushButton_R2Connect.setText("Connect")
            self.pushButton_R2run.setText('Run')
        self.btn_color(self.pushButton_R2Connect, 'green')
        self.pushButton_R2run.setEnabled(False)
        self.btn_color(self.pushButton_R2run, 'gray')

    def camera1_check(self):
        current_mode = self.pushButton_openCamera1.text()
        if current_mode == '打开' or current_mode == 'Open':
            self.camera1()
        elif current_mode == '关闭' or current_mode == 'Close':
            self.camera1_close()

    def camera2_check(self):
        current_mode = self.pushButton_openCamera2.text()
        if current_mode == '打开' or current_mode == 'Open':
            self.camera2()
        elif current_mode == '关闭' or current_mode == 'Close':
            self.camera2_close()

    # 相机线程
    def camera1(self):

        if self.language_mode == '中文':
            self.pushButton_openCamera1.setText("关闭")
        elif self.language_mode == 'English':
            self.pushButton_openCamera1.setText("Close")
        self.btn_color(self.pushButton_openCamera1, 'red')
        try:
            camera1 = threading.Thread(target=self.show_camera1)
            camera1.start()
        except Exception as e:
            e = traceback.format_exc()
            self.showMessageBox_camera()
            self.loger.error(e)

    def camera2(self):

        if self.language_mode == '中文':
            self.pushButton_openCamera2.setText("关闭")
        elif self.language_mode == 'English':
            self.pushButton_openCamera2.setText("Close")
        self.btn_color(self.pushButton_openCamera2, 'red')
        try:
            camera2 = threading.Thread(target=self.show_camera2)
            camera2.start()
        except Exception as e:
            e = traceback.format_exc()
            self.showMessageBox_camera()
            self.loger.error(e)

    def show_camera1(self):
        self.label_camera1_color.show()
        self.label_camera1_depth.show()
        while True:
            rgb = self.r1.capture_thread.rgb_show
            depth = self.r1.capture_thread.depth_show
            rgb_show = QImage(rgb, rgb.shape[1], rgb.shape[0], QImage.Format_RGB888)
            depth_show = QImage(depth, depth.shape[1], depth.shape[0], QImage.Format_RGB888)
            pixmap_color = QPixmap(rgb_show)
            pixmap_color = pixmap_color.scaled(320, 240, Qt.KeepAspectRatio)
            self.label_camera1_color.setPixmap(pixmap_color)
            self.label_camera1_depth.setPixmap(QPixmap.fromImage(depth_show))
            time.sleep(0.5)

    def show_camera2(self):
        self.label_camera2_color.show()
        self.label_camera2_depth.show()
        while True:
            rgb = self.r2.capture_thread.rgb_show
            depth = self.r2.capture_thread.depth_show

            rgb_show = QImage(rgb, rgb.shape[1], rgb.shape[0], QImage.Format_RGB888)
            pixmap_color = QPixmap(rgb_show)
            pixmap_color = pixmap_color.scaled(320, 240, Qt.KeepAspectRatio)

            depth_show = QImage(depth, depth.shape[1], depth.shape[0], QImage.Format_RGB888)
            self.label_camera2_color.setPixmap(pixmap_color)
            self.label_camera2_depth.setPixmap(QPixmap.fromImage(depth_show))
            time.sleep(0.5)

    def camera1_close(self):
        # self.label_camera1_color.clear()
        # self.label_camera1_depth.clear()
        self.label_camera1_color.close()
        self.label_camera1_depth.close()
        if self.language_mode == '中文':
            self.pushButton_openCamera1.setText("打开")
        elif self.language_mode == 'English':
            self.pushButton_openCamera1.setText("Open")
        self.btn_color(self.pushButton_openCamera1, 'blue')

    def camera2_close(self):
        # self.label_camera2_color.clear()
        # self.label_camera2_depth.clear()
        self.label_camera2_color.close()
        self.label_camera2_depth.close()
        if self.language_mode == '中文':
            self.pushButton_openCamera2.setText("打开")
        elif self.language_mode == 'English':
            self.pushButton_openCamera2.setText("Open")
        self.btn_color(self.pushButton_openCamera2, 'blue')

    # 传送带测试
    def conveyor_connect(self):
        self.comboBox_ConveyorPort.setEnabled(False)
        try:
            conveyor_port = self.comboBox_ConveyorPort.currentText()
            self.conveyor = ConveyorMain(conveyor_port)
            self.pushButton_ConveyorOpen.setEnabled(True)
            self.loger.info('Connection Successful')
            self.btn_color(self.pushButton_ConveyorOpen, 'blue')
            if self.language_mode == '中文':
                self.pushButton_ConveyorConnect.setText("断开")
            elif self.language_mode == 'English':
                self.pushButton_ConveyorConnect.setText("Disconnect")
            self.btn_color(self.pushButton_ConveyorConnect, 'red')

        except Exception as e:
            e = traceback.format_exc()
            self.showMessageBox()
            self.comboBox_ConveyorPort.setEnabled(True)
            self.pushButton_ConveyorOpen.setEnabled(False)
            self.btn_color(self.pushButton_ConveyorOpen, 'gray')
            if self.language_mode == '中文':
                self.pushButton_ConveyorConnect.setText('连接')
            elif self.language_mode == 'English':
                self.pushButton_ConveyorConnect.setText('Connect')
            self.btn_color(self.pushButton_ConveyorConnect, 'green')
            self.loger.error(e)

    def conveyor_disconnect(self):
        self.comboBox_ConveyorPort.setEnabled(True)
        self.pushButton_ConveyorOpen.setEnabled(False)
        self.pushButton_ConveyorClose.setEnabled(False)
        self.btn_color(self.pushButton_ConveyorClose, 'gray')
        self.btn_color(self.pushButton_ConveyorOpen, 'gray')
        self.conveyor = None

        if self.language_mode == '中文':
            self.pushButton_ConveyorConnect.setText("连接")
        elif self.language_mode == 'English':
            self.pushButton_ConveyorConnect.setText("Connect")
        self.btn_color(self.pushButton_ConveyorConnect, 'green')
        self.loger.info('Disconnection Successful')

    # 开启传送带
    def open_conveyor(self):
        try:
            self.btn_color(self.pushButton_ConveyorOpen, 'red')
            self.pushButton_ConveyorOpen.setEnabled(False)
            self.pushButton_ConveyorClose.setEnabled(True)
            self.btn_color(self.pushButton_ConveyorClose, 'blue')
            self.conveyor.open_conveyor(5)
            time.sleep(1)
        except Exception as e:
            e = traceback.format_exc()
            self.loger.error(e)

    # 关闭传送带
    def close_conveyor(self):
        try:
            self.btn_color(self.pushButton_ConveyorClose, 'red')
            self.pushButton_ConveyorClose.setEnabled(False)
            self.pushButton_ConveyorOpen.setEnabled(True)
            self.btn_color(self.pushButton_ConveyorOpen, 'blue')
            self.conveyor.close_conveyor()
            time.sleep(1)
        except Exception as e:
            e = traceback.format_exc()
            self.loger.error(e)

    # 获取串口列表
    def get_serial_port_list(self):
        """Get the current serial port and map it to the serial port drop-down box"""
        plist = [
            str(x).split(" - ")[0].strip() for x in serial.tools.list_ports.comports()
        ]
        print('plist:', plist)
        if not plist:
            # if self.comboBox_R1port.currentText() == 'no port':
            #     return
            self.comboBox_R1port.clear()
            self.comboBox_R1port.addItem('No Port')
            self.pushButton_R1Connect.setEnabled(False)
            self.btn_color(self.pushButton_R1Connect, 'gray')
            self.comboBox_R2port.clear()
            self.comboBox_R2port.addItem('No Port')
            self.pushButton_R2Connect.setEnabled(False)
            self.btn_color(self.pushButton_R2Connect, 'gray')
            self.comboBox_ConveyorPort.clear()
            self.comboBox_ConveyorPort.addItem('No Port')
            self.pushButton_ConveyorConnect.setEnabled(False)
            self.btn_color(self.pushButton_ConveyorConnect, 'gray')
            self.port_list = []
            return
        else:
            if self.port_list != plist:
                self.port_list = plist
                self.comboBox_R1port.clear()
                self.comboBox_R2port.clear()
                self.comboBox_ConveyorPort.clear()
                self.pushButton_R1Connect.setEnabled(True)
                self.btn_color(self.pushButton_R1Connect, 'green')
                self.pushButton_R2Connect.setEnabled(True)
                self.btn_color(self.pushButton_R2Connect, 'green')
                self.pushButton_ConveyorConnect.setEnabled(True)
                self.btn_color(self.pushButton_ConveyorConnect, 'green')

                for p in plist:
                    self.comboBox_R1port.addItem(p)
                    self.comboBox_R2port.addItem(p)
                    self.comboBox_ConveyorPort.addItem(p)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SmartKit_APP()
    window.show()

    sys.exit(app.exec_())
