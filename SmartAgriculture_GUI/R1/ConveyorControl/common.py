from enum import Enum

DEBUG = False


# 地址帧
class DeviceAdress(Enum):
    IR_DETECT = 0x21
    STEPPER_MOTOR_42 = 0x30
    STEPPER_MOTOR_57 = 0x31


# 指令帧
class Command(Enum):
    GET_TOF_DISTANCE = 0x51
    SET_DIR = 0xA0
    SET_SPEED = 0xA1
    GET_DIR = 0xA2
    GET_SPEED = 0xA3
    GET_DISTANCE = 0xA4
    WRITE_STEPS_BY_SWITCH = 0xA5
    WRITE_ANGLE = 0xA6
    WRITE_STEPS = 0xA7
    WRITE_DISTANCE_ZERO = 0xA8
    WRITE_DISTANCE = 0xA9


# 开关类型
class SwitchMode(Enum):
    CLOSE = 0
    OPEN = 1


# 电机、舵机方向类型
class MotorDirection(Enum):
    CLOCKWISE = 0x0
    COUNTCLOCKWISE = 0x1


# 步进电机步进类型
class MotorInterfaceType(Enum):
    FUNCTION = 0
    DRIVER = 1
    FULL2WIRE = 2
    FULL3WIRE = 3
    FULL4WIRE = 4
    HALF3WIRE = 6
    HALF4WIRE = 8
    HALF8WIRE = 16


# 步进电机类型
class StepperMotorType(Enum):
    STEPPER_MOTOR_42 = 1
    STEPPER_MOTOR_57 = 2