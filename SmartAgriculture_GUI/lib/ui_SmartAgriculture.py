# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SmartAgriculturelhXGHa.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1150, 943)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frame_3 = QFrame(self.centralwidget)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(20, 240, 391, 221))
        self.frame_3.setAutoFillBackground(False)
        self.frame_3.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius:10px;\n"
"border-style:outset;")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.formLayoutWidget = QWidget(self.frame_3)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(20, 20, 351, 181))
        self.formLayout_5 = QFormLayout(self.formLayoutWidget)
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.formLayout_5.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_13 = QLineEdit(self.formLayoutWidget)
        self.lineEdit_13.setObjectName(u"lineEdit_13")
        self.lineEdit_13.setMinimumSize(QSize(180, 30))
        self.lineEdit_13.setMaximumSize(QSize(180, 30))
        font = QFont()
        font.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(False)
        self.lineEdit_13.setFont(font)
        self.lineEdit_13.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.lineEdit_13.setText(u"\u91c7\u6458\u673a\u5668\u4eba")
        self.lineEdit_13.setMaxLength(80)
        self.lineEdit_13.setFrame(False)
        self.lineEdit_13.setDragEnabled(False)
        self.lineEdit_13.setReadOnly(True)

        self.formLayout_5.setWidget(0, QFormLayout.LabelRole, self.lineEdit_13)

        self.lineEdit_17 = QLineEdit(self.formLayoutWidget)
        self.lineEdit_17.setObjectName(u"lineEdit_17")
        self.lineEdit_17.setMinimumSize(QSize(180, 30))
        self.lineEdit_17.setMaximumSize(QSize(180, 30))
        font1 = QFont()
        font1.setFamily(u"\u5b8b\u4f53")
        font1.setPointSize(9)
        font1.setBold(False)
        font1.setWeight(50)
        self.lineEdit_17.setFont(font1)
        self.lineEdit_17.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.lineEdit_17.setFrame(False)

        self.formLayout_5.setWidget(1, QFormLayout.LabelRole, self.lineEdit_17)

        self.comboBox_R1device = QComboBox(self.formLayoutWidget)
        self.comboBox_R1device.addItem("")
        self.comboBox_R1device.setObjectName(u"comboBox_R1device")
        self.comboBox_R1device.setMinimumSize(QSize(160, 30))
        self.comboBox_R1device.setMaximumSize(QSize(160, 30))
        self.comboBox_R1device.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-style:inset;\n"
"border:2px groove gray;\n"
"border-radius:0px;")

        self.formLayout_5.setWidget(1, QFormLayout.FieldRole, self.comboBox_R1device)

        self.lineEdit_16 = QLineEdit(self.formLayoutWidget)
        self.lineEdit_16.setObjectName(u"lineEdit_16")
        self.lineEdit_16.setMinimumSize(QSize(180, 30))
        self.lineEdit_16.setMaximumSize(QSize(160, 30))
        self.lineEdit_16.setFont(font1)
        self.lineEdit_16.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.lineEdit_16.setFrame(False)

        self.formLayout_5.setWidget(2, QFormLayout.LabelRole, self.lineEdit_16)

        self.comboBox_R1port = QComboBox(self.formLayoutWidget)
        self.comboBox_R1port.addItem("")
        self.comboBox_R1port.setObjectName(u"comboBox_R1port")
        self.comboBox_R1port.setMinimumSize(QSize(160, 30))
        self.comboBox_R1port.setMaximumSize(QSize(160, 30))
        self.comboBox_R1port.setFont(font1)
        self.comboBox_R1port.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-style:inset;\n"
"border:2px groove gray;\n"
"border-radius:0px;")

        self.formLayout_5.setWidget(2, QFormLayout.FieldRole, self.comboBox_R1port)

        self.lineEdit_18 = QLineEdit(self.formLayoutWidget)
        self.lineEdit_18.setObjectName(u"lineEdit_18")
        self.lineEdit_18.setMinimumSize(QSize(180, 30))
        self.lineEdit_18.setMaximumSize(QSize(180, 30))
        self.lineEdit_18.setFont(font1)
        self.lineEdit_18.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.lineEdit_18.setFrame(False)

        self.formLayout_5.setWidget(3, QFormLayout.LabelRole, self.lineEdit_18)

        self.comboBox_R1baud = QComboBox(self.formLayoutWidget)
        self.comboBox_R1baud.addItem("")
        self.comboBox_R1baud.addItem("")
        self.comboBox_R1baud.setObjectName(u"comboBox_R1baud")
        self.comboBox_R1baud.setMinimumSize(QSize(150, 30))
        self.comboBox_R1baud.setMaximumSize(QSize(160, 30))
        self.comboBox_R1baud.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-style:inset;\n"
"border:2px groove gray;\n"
"border-radius:0px;")

        self.formLayout_5.setWidget(3, QFormLayout.FieldRole, self.comboBox_R1baud)

        self.pushButton_R1run = QPushButton(self.formLayoutWidget)
        self.pushButton_R1run.setObjectName(u"pushButton_R1run")
        self.pushButton_R1run.setMinimumSize(QSize(310, 30))
        self.pushButton_R1run.setMaximumSize(QSize(350, 30))
        font2 = QFont()
        font2.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font2.setPointSize(10)
        font2.setBold(True)
        font2.setWeight(75)
        self.pushButton_R1run.setFont(font2)
        self.pushButton_R1run.setLayoutDirection(Qt.RightToLeft)
        self.pushButton_R1run.setAutoFillBackground(False)
        self.pushButton_R1run.setStyleSheet(u"background-color: rgb(41, 128, 185);\n"
"color: rgb(255, 255, 255);\n"
"border-radius:10px;\n"
"border:2px groove gray;\n"
"border-style:outset;")

        self.formLayout_5.setWidget(4, QFormLayout.SpanningRole, self.pushButton_R1run)

        self.pushButton_R1Connect = QPushButton(self.formLayoutWidget)
        self.pushButton_R1Connect.setObjectName(u"pushButton_R1Connect")
        self.pushButton_R1Connect.setMinimumSize(QSize(160, 30))
        self.pushButton_R1Connect.setMaximumSize(QSize(160, 30))
        self.pushButton_R1Connect.setFont(font2)
        self.pushButton_R1Connect.setAutoFillBackground(False)
        self.pushButton_R1Connect.setStyleSheet(u"background-color: rgb(41, 128, 185);\n"
"color: rgb(255, 255, 255);\n"
"border-radius:10px;\n"
"border:2px groove gray;\n"
"border-style:outset;")
        self.pushButton_R1Connect.setIconSize(QSize(40, 30))
        self.pushButton_R1Connect.setAutoDefault(False)
        self.pushButton_R1Connect.setFlat(False)

        self.formLayout_5.setWidget(0, QFormLayout.FieldRole, self.pushButton_R1Connect)

        self.frame_4 = QFrame(self.centralwidget)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setGeometry(QRect(20, 490, 391, 221))
        self.frame_4.setAutoFillBackground(False)
        self.frame_4.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-style:outset;\n"
"border-radius:10px;")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.formLayoutWidget_3 = QWidget(self.frame_4)
        self.formLayoutWidget_3.setObjectName(u"formLayoutWidget_3")
        self.formLayoutWidget_3.setGeometry(QRect(20, 20, 351, 183))
        self.formLayout_6 = QFormLayout(self.formLayoutWidget_3)
        self.formLayout_6.setObjectName(u"formLayout_6")
        self.formLayout_6.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_7 = QLineEdit(self.formLayoutWidget_3)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setMinimumSize(QSize(180, 30))
        self.lineEdit_7.setMaximumSize(QSize(150, 30))
        self.lineEdit_7.setFont(font)
        self.lineEdit_7.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.lineEdit_7.setText(u"\u5206\u62e3\u673a\u5668\u4eba")
        self.lineEdit_7.setMaxLength(80)
        self.lineEdit_7.setFrame(False)
        self.lineEdit_7.setDragEnabled(False)
        self.lineEdit_7.setReadOnly(True)

        self.formLayout_6.setWidget(0, QFormLayout.LabelRole, self.lineEdit_7)

        self.pushButton_R2Connect = QPushButton(self.formLayoutWidget_3)
        self.pushButton_R2Connect.setObjectName(u"pushButton_R2Connect")
        self.pushButton_R2Connect.setMinimumSize(QSize(160, 30))
        self.pushButton_R2Connect.setMaximumSize(QSize(160, 30))
        self.pushButton_R2Connect.setFont(font2)
        self.pushButton_R2Connect.setLayoutDirection(Qt.RightToLeft)
        self.pushButton_R2Connect.setAutoFillBackground(False)
        self.pushButton_R2Connect.setStyleSheet(u"background-color:rgb(41, 128, 185);\n"
"color: rgb(255, 255, 255);\n"
"border-radius:10px;\n"
"border:2px groove gray;\n"
"border-style:outset;")
        self.pushButton_R2Connect.setIconSize(QSize(40, 30))
        self.pushButton_R2Connect.setAutoDefault(False)
        self.pushButton_R2Connect.setFlat(False)

        self.formLayout_6.setWidget(0, QFormLayout.FieldRole, self.pushButton_R2Connect)

        self.lineEdit_9 = QLineEdit(self.formLayoutWidget_3)
        self.lineEdit_9.setObjectName(u"lineEdit_9")
        self.lineEdit_9.setMinimumSize(QSize(160, 30))
        self.lineEdit_9.setMaximumSize(QSize(160, 30))
        self.lineEdit_9.setFont(font1)
        self.lineEdit_9.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.lineEdit_9.setFrame(False)

        self.formLayout_6.setWidget(1, QFormLayout.LabelRole, self.lineEdit_9)

        self.comboBox_R2device = QComboBox(self.formLayoutWidget_3)
        self.comboBox_R2device.addItem("")
        self.comboBox_R2device.setObjectName(u"comboBox_R2device")
        self.comboBox_R2device.setEnabled(True)
        self.comboBox_R2device.setMinimumSize(QSize(150, 30))
        self.comboBox_R2device.setMaximumSize(QSize(160, 30))
        self.comboBox_R2device.setBaseSize(QSize(170, 20))
        self.comboBox_R2device.setLayoutDirection(Qt.LeftToRight)
        self.comboBox_R2device.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-style:inset;\n"
"border:2px groove gray;\n"
"border-radius:0px;")

        self.formLayout_6.setWidget(1, QFormLayout.FieldRole, self.comboBox_R2device)

        self.lineEdit_8 = QLineEdit(self.formLayoutWidget_3)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        self.lineEdit_8.setMinimumSize(QSize(160, 30))
        self.lineEdit_8.setMaximumSize(QSize(160, 30))
        self.lineEdit_8.setFont(font1)
        self.lineEdit_8.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.lineEdit_8.setFrame(False)

        self.formLayout_6.setWidget(2, QFormLayout.LabelRole, self.lineEdit_8)

        self.lineEdit_10 = QLineEdit(self.formLayoutWidget_3)
        self.lineEdit_10.setObjectName(u"lineEdit_10")
        self.lineEdit_10.setMinimumSize(QSize(160, 30))
        self.lineEdit_10.setMaximumSize(QSize(160, 30))
        self.lineEdit_10.setFont(font1)
        self.lineEdit_10.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.lineEdit_10.setFrame(False)

        self.formLayout_6.setWidget(3, QFormLayout.LabelRole, self.lineEdit_10)

        self.comboBox_R2baud = QComboBox(self.formLayoutWidget_3)
        self.comboBox_R2baud.addItem("")
        self.comboBox_R2baud.addItem("")
        self.comboBox_R2baud.setObjectName(u"comboBox_R2baud")
        self.comboBox_R2baud.setMinimumSize(QSize(150, 30))
        self.comboBox_R2baud.setMaximumSize(QSize(160, 30))
        self.comboBox_R2baud.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-style:inset;\n"
"border:2px groove gray;\n"
"border-radius:0px;")

        self.formLayout_6.setWidget(3, QFormLayout.FieldRole, self.comboBox_R2baud)

        self.pushButton_R2run = QPushButton(self.formLayoutWidget_3)
        self.pushButton_R2run.setObjectName(u"pushButton_R2run")
        self.pushButton_R2run.setMinimumSize(QSize(310, 30))
        self.pushButton_R2run.setMaximumSize(QSize(350, 30))
        self.pushButton_R2run.setFont(font2)
        self.pushButton_R2run.setLayoutDirection(Qt.LeftToRight)
        self.pushButton_R2run.setAutoFillBackground(False)
        self.pushButton_R2run.setStyleSheet(u"background-color: rgb(41, 128, 185);\n"
"color: rgb(255, 255, 255);\n"
"border-radius:10px;\n"
"border:2px groove gray;\n"
"border-style:outset;")

        self.formLayout_6.setWidget(4, QFormLayout.SpanningRole, self.pushButton_R2run)

        self.comboBox_R2port = QComboBox(self.formLayoutWidget_3)
        self.comboBox_R2port.addItem("")
        self.comboBox_R2port.setObjectName(u"comboBox_R2port")
        self.comboBox_R2port.setEnabled(True)
        self.comboBox_R2port.setMinimumSize(QSize(150, 30))
        self.comboBox_R2port.setMaximumSize(QSize(160, 30))
        self.comboBox_R2port.setBaseSize(QSize(120, 20))
        self.comboBox_R2port.setFont(font1)
        self.comboBox_R2port.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-style:inset;\n"
"border:2px groove gray;\n"
"border-radius:0px;")
        self.comboBox_R2port.setIconSize(QSize(40, 20))

        self.formLayout_6.setWidget(2, QFormLayout.FieldRole, self.comboBox_R2port)

        self.frame_5 = QFrame(self.centralwidget)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setGeometry(QRect(20, 740, 391, 151))
        self.frame_5.setAutoFillBackground(False)
        self.frame_5.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-style:outset;\n"
"border-radius:10px;")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.formLayoutWidget_4 = QWidget(self.frame_5)
        self.formLayoutWidget_4.setObjectName(u"formLayoutWidget_4")
        self.formLayoutWidget_4.setGeometry(QRect(20, 20, 351, 111))
        self.formLayout_7 = QFormLayout(self.formLayoutWidget_4)
        self.formLayout_7.setObjectName(u"formLayout_7")
        self.formLayout_7.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_19 = QLineEdit(self.formLayoutWidget_4)
        self.lineEdit_19.setObjectName(u"lineEdit_19")
        self.lineEdit_19.setMinimumSize(QSize(170, 30))
        self.lineEdit_19.setMaximumSize(QSize(180, 30))
        self.lineEdit_19.setFont(font)
        self.lineEdit_19.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.lineEdit_19.setText(u"\u4f20\u9001\u5e26")
        self.lineEdit_19.setMaxLength(80)
        self.lineEdit_19.setFrame(False)
        self.lineEdit_19.setDragEnabled(False)
        self.lineEdit_19.setReadOnly(True)

        self.formLayout_7.setWidget(0, QFormLayout.LabelRole, self.lineEdit_19)

        self.lineEdit_20 = QLineEdit(self.formLayoutWidget_4)
        self.lineEdit_20.setObjectName(u"lineEdit_20")
        self.lineEdit_20.setMinimumSize(QSize(170, 30))
        self.lineEdit_20.setMaximumSize(QSize(160, 30))
        self.lineEdit_20.setFont(font1)
        self.lineEdit_20.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.lineEdit_20.setFrame(False)

        self.formLayout_7.setWidget(1, QFormLayout.LabelRole, self.lineEdit_20)

        self.comboBox_ConveyorPort = QComboBox(self.formLayoutWidget_4)
        self.comboBox_ConveyorPort.addItem("")
        self.comboBox_ConveyorPort.setObjectName(u"comboBox_ConveyorPort")
        self.comboBox_ConveyorPort.setMinimumSize(QSize(170, 30))
        self.comboBox_ConveyorPort.setMaximumSize(QSize(160, 30))
        self.comboBox_ConveyorPort.setFont(font1)
        self.comboBox_ConveyorPort.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"border-style:inset;\n"
"border:2px groove gray;\n"
"border-radius:0px;")

        self.formLayout_7.setWidget(1, QFormLayout.FieldRole, self.comboBox_ConveyorPort)

        self.pushButton_ConveyorOpen = QPushButton(self.formLayoutWidget_4)
        self.pushButton_ConveyorOpen.setObjectName(u"pushButton_ConveyorOpen")
        self.pushButton_ConveyorOpen.setMinimumSize(QSize(170, 30))
        self.pushButton_ConveyorOpen.setMaximumSize(QSize(160, 30))
        self.pushButton_ConveyorOpen.setFont(font2)
        self.pushButton_ConveyorOpen.setLayoutDirection(Qt.LeftToRight)
        self.pushButton_ConveyorOpen.setAutoFillBackground(False)
        self.pushButton_ConveyorOpen.setStyleSheet(u"background-color: rgb(41, 128, 185);\n"
"color: rgb(255, 255, 255);\n"
"border-radius:10px;\n"
"border:2px groove gray;\n"
"border-style:outset;")

        self.formLayout_7.setWidget(2, QFormLayout.LabelRole, self.pushButton_ConveyorOpen)

        self.pushButton_ConveyorClose = QPushButton(self.formLayoutWidget_4)
        self.pushButton_ConveyorClose.setObjectName(u"pushButton_ConveyorClose")
        self.pushButton_ConveyorClose.setMinimumSize(QSize(170, 30))
        self.pushButton_ConveyorClose.setMaximumSize(QSize(160, 30))
        self.pushButton_ConveyorClose.setFont(font2)
        self.pushButton_ConveyorClose.setLayoutDirection(Qt.RightToLeft)
        self.pushButton_ConveyorClose.setAutoFillBackground(False)
        self.pushButton_ConveyorClose.setStyleSheet(u"background-color: rgb(41, 128, 185);\n"
"color: rgb(255, 255, 255);\n"
"border-radius:10px;\n"
"border:2px groove gray;\n"
"border-style:outset;")

        self.formLayout_7.setWidget(2, QFormLayout.FieldRole, self.pushButton_ConveyorClose)

        self.pushButton_ConveyorConnect = QPushButton(self.formLayoutWidget_4)
        self.pushButton_ConveyorConnect.setObjectName(u"pushButton_ConveyorConnect")
        self.pushButton_ConveyorConnect.setMinimumSize(QSize(170, 30))
        self.pushButton_ConveyorConnect.setMaximumSize(QSize(160, 30))
        self.pushButton_ConveyorConnect.setFont(font2)
        self.pushButton_ConveyorConnect.setAutoFillBackground(False)
        self.pushButton_ConveyorConnect.setStyleSheet(u"background-color: rgb(41, 128, 185);\n"
"color: rgb(255, 255, 255);\n"
"border-radius:10px;\n"
"border:2px groove gray;\n"
"border-style:outset;")
        self.pushButton_ConveyorConnect.setIconSize(QSize(40, 30))
        self.pushButton_ConveyorConnect.setAutoDefault(False)
        self.pushButton_ConveyorConnect.setFlat(False)

        self.formLayout_7.setWidget(0, QFormLayout.FieldRole, self.pushButton_ConveyorConnect)

        self.frame_6 = QFrame(self.centralwidget)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setGeometry(QRect(440, 740, 691, 151))
        self.frame_6.setAutoFillBackground(False)
        self.frame_6.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-style:outset;\n"
"border-radius:10px;")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayoutWidget_3 = QWidget(self.frame_6)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(19, 19, 651, 121))
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_pixelcoords = QLabel(self.gridLayoutWidget_3)
        self.label_pixelcoords.setObjectName(u"label_pixelcoords")
        self.label_pixelcoords.setMinimumSize(QSize(100, 30))
        self.label_pixelcoords.setMaximumSize(QSize(320, 30))
        font3 = QFont()
        font3.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font3.setPointSize(10)
        self.label_pixelcoords.setFont(font3)
        self.label_pixelcoords.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_3.addWidget(self.label_pixelcoords, 1, 1, 1, 1)

        self.lineEdit_23 = QLineEdit(self.gridLayoutWidget_3)
        self.lineEdit_23.setObjectName(u"lineEdit_23")
        self.lineEdit_23.setMinimumSize(QSize(370, 30))
        self.lineEdit_23.setMaximumSize(QSize(320, 30))
        self.lineEdit_23.setFont(font)
        self.lineEdit_23.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.lineEdit_23.setText(u"\u5750\u6807\u663e\u793a")
        self.lineEdit_23.setMaxLength(80)
        self.lineEdit_23.setFrame(False)
        self.lineEdit_23.setDragEnabled(False)
        self.lineEdit_23.setReadOnly(True)

        self.gridLayout_3.addWidget(self.lineEdit_23, 0, 0, 1, 1)

        self.pushButton_showPixelCoords = QPushButton(self.gridLayoutWidget_3)
        self.pushButton_showPixelCoords.setObjectName(u"pushButton_showPixelCoords")
        self.pushButton_showPixelCoords.setMinimumSize(QSize(370, 30))
        self.pushButton_showPixelCoords.setMaximumSize(QSize(370, 30))
        self.pushButton_showPixelCoords.setFont(font2)
        self.pushButton_showPixelCoords.setLayoutDirection(Qt.LeftToRight)
        self.pushButton_showPixelCoords.setAutoFillBackground(False)
        self.pushButton_showPixelCoords.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(41, 128, 185);\n"
"border-radius:10px;\n"
"border:2px groove gray;\n"
"border-style:outset;")

        self.gridLayout_3.addWidget(self.pushButton_showPixelCoords, 1, 0, 1, 1)

        self.pushButton_showRealCoords = QPushButton(self.gridLayoutWidget_3)
        self.pushButton_showRealCoords.setObjectName(u"pushButton_showRealCoords")
        self.pushButton_showRealCoords.setMinimumSize(QSize(370, 30))
        self.pushButton_showRealCoords.setMaximumSize(QSize(300, 30))
        self.pushButton_showRealCoords.setFont(font2)
        self.pushButton_showRealCoords.setLayoutDirection(Qt.LeftToRight)
        self.pushButton_showRealCoords.setAutoFillBackground(False)
        self.pushButton_showRealCoords.setStyleSheet(u"background-color: rgb(41, 128, 185);\n"
"color: rgb(255, 255, 255);\n"
"border-radius:10px;\n"
"border:2px groove gray;\n"
"border-style:outset;")

        self.gridLayout_3.addWidget(self.pushButton_showRealCoords, 2, 0, 1, 1)

        self.label_realcoords = QLabel(self.gridLayoutWidget_3)
        self.label_realcoords.setObjectName(u"label_realcoords")
        self.label_realcoords.setMinimumSize(QSize(100, 30))
        self.label_realcoords.setMaximumSize(QSize(320, 30))
        self.label_realcoords.setFont(font3)
        self.label_realcoords.setLayoutDirection(Qt.LeftToRight)
        self.label_realcoords.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_3.addWidget(self.label_realcoords, 2, 1, 1, 1)

        self.frame_7 = QFrame(self.centralwidget)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setGeometry(QRect(440, 20, 691, 331))
        self.frame_7.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-style:outset;\n"
"border-radius:10px;\n"
"")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.gridLayoutWidget_2 = QWidget(self.frame_7)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(20, 20, 651, 291))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_openCamera1 = QPushButton(self.gridLayoutWidget_2)
        self.pushButton_openCamera1.setObjectName(u"pushButton_openCamera1")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_openCamera1.sizePolicy().hasHeightForWidth())
        self.pushButton_openCamera1.setSizePolicy(sizePolicy)
        self.pushButton_openCamera1.setMinimumSize(QSize(30, 30))
        self.pushButton_openCamera1.setMaximumSize(QSize(150, 30))
        self.pushButton_openCamera1.setFont(font2)
        self.pushButton_openCamera1.setMouseTracking(False)
        self.pushButton_openCamera1.setLayoutDirection(Qt.RightToLeft)
        self.pushButton_openCamera1.setAutoFillBackground(False)
        self.pushButton_openCamera1.setStyleSheet(u"background-color: rgb(41, 128, 185);\n"
"color: rgb(255, 255, 255);\n"
"border-radius:10px;\n"
"border:2px groove gray;\n"
"border-style:outset;")
        self.pushButton_openCamera1.setIconSize(QSize(40, 30))
        self.pushButton_openCamera1.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButton_openCamera1, 0, 1, 1, 1)

        self.lineEdit_24 = QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_24.setObjectName(u"lineEdit_24")
        self.lineEdit_24.setMinimumSize(QSize(320, 30))
        self.lineEdit_24.setMaximumSize(QSize(320, 30))
        self.lineEdit_24.setFont(font)
        self.lineEdit_24.setContextMenuPolicy(Qt.NoContextMenu)
        self.lineEdit_24.setLayoutDirection(Qt.RightToLeft)
        self.lineEdit_24.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.lineEdit_24.setText(u"\u679c\u68113D\u76f8\u673a\u753b\u9762")
        self.lineEdit_24.setMaxLength(80)
        self.lineEdit_24.setFrame(False)
        self.lineEdit_24.setDragEnabled(False)
        self.lineEdit_24.setReadOnly(True)

        self.gridLayout_2.addWidget(self.lineEdit_24, 0, 0, 1, 1)

        self.label_camera1_depth = QLabel(self.gridLayoutWidget_2)
        self.label_camera1_depth.setObjectName(u"label_camera1_depth")
        self.label_camera1_depth.setMinimumSize(QSize(320, 240))
        self.label_camera1_depth.setMaximumSize(QSize(320, 240))
        self.label_camera1_depth.setLayoutDirection(Qt.RightToLeft)

        self.gridLayout_2.addWidget(self.label_camera1_depth, 1, 1, 1, 1)

        self.label_camera1_color = QLabel(self.gridLayoutWidget_2)
        self.label_camera1_color.setObjectName(u"label_camera1_color")
        self.label_camera1_color.setMinimumSize(QSize(320, 240))
        self.label_camera1_color.setMaximumSize(QSize(320, 240))

        self.gridLayout_2.addWidget(self.label_camera1_color, 1, 0, 1, 1)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(440, 380, 691, 331))
        self.frame.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-style:outset;\n"
"border-radius:10px;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayoutWidget = QWidget(self.frame)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(19, 20, 651, 291))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_25 = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_25.setObjectName(u"lineEdit_25")
        self.lineEdit_25.setMinimumSize(QSize(320, 30))
        self.lineEdit_25.setMaximumSize(QSize(320, 30))
        self.lineEdit_25.setFont(font)
        self.lineEdit_25.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.lineEdit_25.setText(u"\u4f20\u9001\u5e263D\u76f8\u673a\u753b\u9762")
        self.lineEdit_25.setMaxLength(80)
        self.lineEdit_25.setFrame(False)
        self.lineEdit_25.setDragEnabled(False)
        self.lineEdit_25.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_25, 0, 0, 1, 1)

        self.label_camera2_color = QLabel(self.gridLayoutWidget)
        self.label_camera2_color.setObjectName(u"label_camera2_color")
        self.label_camera2_color.setMinimumSize(QSize(320, 240))
        self.label_camera2_color.setMaximumSize(QSize(320, 240))

        self.gridLayout.addWidget(self.label_camera2_color, 1, 0, 1, 1)

        self.label_camera2_depth = QLabel(self.gridLayoutWidget)
        self.label_camera2_depth.setObjectName(u"label_camera2_depth")
        self.label_camera2_depth.setMinimumSize(QSize(320, 240))
        self.label_camera2_depth.setMaximumSize(QSize(320, 240))

        self.gridLayout.addWidget(self.label_camera2_depth, 1, 1, 1, 1)

        self.pushButton_openCamera2 = QPushButton(self.gridLayoutWidget)
        self.pushButton_openCamera2.setObjectName(u"pushButton_openCamera2")
        self.pushButton_openCamera2.setMinimumSize(QSize(150, 30))
        self.pushButton_openCamera2.setMaximumSize(QSize(150, 30))
        self.pushButton_openCamera2.setFont(font2)
        self.pushButton_openCamera2.setLayoutDirection(Qt.RightToLeft)
        self.pushButton_openCamera2.setAutoFillBackground(False)
        self.pushButton_openCamera2.setStyleSheet(u"background-color:rgb(41, 128, 185);\n"
"color: rgb(255, 255, 255);\n"
"border-radius:10px;\n"
"border:2px groove gray;\n"
"border-style:outset;")
        self.pushButton_openCamera2.setIconSize(QSize(40, 30))
        self.pushButton_openCamera2.setAutoDefault(False)
        self.pushButton_openCamera2.setFlat(False)

        self.gridLayout.addWidget(self.pushButton_openCamera2, 0, 1, 1, 1)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(20, 130, 391, 81))
        self.frame_2.setAutoFillBackground(False)
        self.frame_2.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius:10px;\n"
"")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayoutWidget = QWidget(self.frame_2)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(20, 20, 351, 41))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_language = QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_language.setObjectName(u"lineEdit_language")
        self.lineEdit_language.setMinimumSize(QSize(100, 30))
        self.lineEdit_language.setMaximumSize(QSize(130, 30))
        self.lineEdit_language.setFont(font)
        self.lineEdit_language.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.lineEdit_language.setText(u"\u8bed\u8a00/Language")
        self.lineEdit_language.setMaxLength(80)
        self.lineEdit_language.setFrame(False)
        self.lineEdit_language.setDragEnabled(False)
        self.lineEdit_language.setReadOnly(True)

        self.horizontalLayout.addWidget(self.lineEdit_language)

        self.comboBox_language = QComboBox(self.horizontalLayoutWidget)
        self.comboBox_language.addItem("")
        self.comboBox_language.addItem("")
        self.comboBox_language.setObjectName(u"comboBox_language")
        self.comboBox_language.setMinimumSize(QSize(90, 30))
        self.comboBox_language.setMaximumSize(QSize(90, 30))
        self.comboBox_language.setStyleSheet(u"border-style:inset;\n"
"border:2px groove gray;\n"
"border-radius:0px;")

        self.horizontalLayout.addWidget(self.comboBox_language)

        self.pushButton_language = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_language.setObjectName(u"pushButton_language")
        self.pushButton_language.setMinimumSize(QSize(80, 30))
        self.pushButton_language.setMaximumSize(QSize(80, 30))
        self.pushButton_language.setFont(font2)
        self.pushButton_language.setAutoFillBackground(False)
        self.pushButton_language.setStyleSheet(u"background-color: rgb(41, 128, 185);\n"
"color: rgb(255, 255, 255);\n"
"border-radius:10px;\n"
"border:2px groove gray;\n"
"border-style:outset;")
        self.pushButton_language.setIconSize(QSize(40, 30))
        self.pushButton_language.setAutoDefault(False)
        self.pushButton_language.setFlat(False)

        self.horizontalLayout.addWidget(self.pushButton_language)

        self.label_logo = QLabel(self.centralwidget)
        self.label_logo.setObjectName(u"label_logo")
        self.label_logo.setGeometry(QRect(40, 30, 311, 81))
        self.label_logo.setPixmap(QPixmap(u"./lib/logo.png"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1150, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"SmartAgriculture_3D", None))
        self.lineEdit_17.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u5907", None))
        self.comboBox_R1device.setItemText(0, QCoreApplication.translate("MainWindow", u"mechArm270 M5", None))

        self.lineEdit_16.setText(QCoreApplication.translate("MainWindow", u"\u4e32\u53e3", None))
        self.comboBox_R1port.setItemText(0, QCoreApplication.translate("MainWindow", u"no port", None))

        self.lineEdit_18.setText(QCoreApplication.translate("MainWindow", u"\u6ce2\u7279\u7387", None))
        self.comboBox_R1baud.setItemText(0, QCoreApplication.translate("MainWindow", u"115200", None))
        self.comboBox_R1baud.setItemText(1, QCoreApplication.translate("MainWindow", u"1000000", None))

        self.pushButton_R1run.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u884c", None))
        self.pushButton_R1Connect.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5", None))
        self.pushButton_R2Connect.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5", None))
        self.lineEdit_9.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u5907", None))
        self.comboBox_R2device.setItemText(0, QCoreApplication.translate("MainWindow", u"mechArm270 M5", None))

        self.lineEdit_8.setText(QCoreApplication.translate("MainWindow", u"\u4e32\u53e3", None))
        self.lineEdit_10.setText(QCoreApplication.translate("MainWindow", u"\u6ce2\u7279\u7387", None))
        self.comboBox_R2baud.setItemText(0, QCoreApplication.translate("MainWindow", u"115200", None))
        self.comboBox_R2baud.setItemText(1, QCoreApplication.translate("MainWindow", u"1000000", None))

        self.pushButton_R2run.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u884c", None))
        self.comboBox_R2port.setItemText(0, QCoreApplication.translate("MainWindow", u"no port", None))

        self.lineEdit_20.setText(QCoreApplication.translate("MainWindow", u"\u4e32\u53e3", None))
        self.comboBox_ConveyorPort.setItemText(0, QCoreApplication.translate("MainWindow", u"no port", None))

        self.pushButton_ConveyorOpen.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00", None))
        self.pushButton_ConveyorClose.setText(QCoreApplication.translate("MainWindow", u"\u5173\u95ed", None))
        self.pushButton_ConveyorConnect.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5", None))
        self.label_pixelcoords.setText("")
        self.pushButton_showPixelCoords.setText(QCoreApplication.translate("MainWindow", u"\u679c\u5b50\u5750\u6807\uff08\u76f8\u5bf9\u4e8e\u76f8\u673a\uff09", None))
        self.pushButton_showRealCoords.setText(QCoreApplication.translate("MainWindow", u"\u679c\u5b50\u5750\u6807\uff08\u76f8\u5bf9\u4e8e\u673a\u68b0\u81c2\uff09", None))
        self.label_realcoords.setText("")
        self.pushButton_openCamera1.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00", None))
        self.label_camera1_depth.setText("")
        self.label_camera1_color.setText("")
        self.label_camera2_color.setText("")
        self.label_camera2_depth.setText("")
        self.pushButton_openCamera2.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00", None))
        self.comboBox_language.setItemText(0, QCoreApplication.translate("MainWindow", u"\u4e2d\u6587", None))
        self.comboBox_language.setItemText(1, QCoreApplication.translate("MainWindow", u"English", None))

        self.pushButton_language.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58", None))
        self.label_logo.setText("")
    # retranslateUi

