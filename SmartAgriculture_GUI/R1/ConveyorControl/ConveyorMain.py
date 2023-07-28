from R1.ConveyorControl.common import *
from serial import Serial
import struct
import time


class ConveyorMain(object):
    read_delay = 0.1               # 读指令间隔
    invalid_data = -1              # 无效数据帧
    command_header = 0xff          # 指令帧头
    length = 0                     # 指令长度
    content = []                   # 指令数据
    cmd = 0                        # 指令帧
    check_digit_user = 0           # 用户ADD8校验
    check_digit_ok = invalid_data  # 指令正确ADD8校验
    check_digit_flag = False       # 指令校验标志

    def __init__(self, port, baudrate="115200", timeout=0.1, debug=False):
        self._serial_port = Serial()
        self._serial_port.port = port
        self._serial_port.baudrate = baudrate
        self._serial_port.timeout = timeout
        self._serial_port.rts = True
        self._serial_port.dtr = True
        self._serial_port.open()

    # 关闭串口
    def __destroy__(self):
        self._serial_port.close()

    # 刷新串口
    def flush(self):
        self._serial_port.flush()

    
    # 指令双帧头范围检查
    def double_header_check(self, read_buff):
        if len(read_buff) >= 2:
            if self.command_header == read_buff[0] and self.command_header == read_buff[1]:
                return True
        return False
    
    # 计算指令ADD8校验位
    def check_digit(self, cmd, content):
        ver = cmd
        if 0 < len(content):
            for item in content:
                ver += item
        ver &= 0xff
        self.check_digit_flag = True
        return ver

    # 读取下位机指令数据
    def read(self):
        time.sleep(self.read_delay)

        if self._serial_port.inWaiting() <= 0:
            return False
        
        read_buff = self._serial_port.read(self._serial_port.inWaiting())
        if len(read_buff) < 6 or not self.double_header_check(read_buff):
            return False
        else:
            if DEBUG == True:
                print("Read timeout ! ")
            else:
                pass

        self.length = read_buff[3]
        self.content = []
        content_begin = 4
        if self.length == 0:
            self.cmd = read_buff[content_begin]
            self.check_digit_user = read_buff[content_begin + 1]
        else:
            content_end = content_begin + self.length
            self.content = read_buff[content_begin: content_end]
            self.cmd = read_buff[content_end]
            self.check_digit_user = read_buff[content_end + 1]
        self.check_digit_ok = self.check_digit(self.cmd, self.content)

        if DEBUG == True:
            print("content: ", self.content)

        if self.check_digit_flag:
            return True
        else:
            return False
        
    # 写指令数据到下位机
    def write(self, adress, content, command):
        data = [self.command_header, self.command_header, adress, len(content), *content, command, self.check_digit(command, content)]
        if DEBUG == True:
            print("write data: ", data)

        self._serial_port.flush()
        self._serial_port.write(data)

    # 获取下位机返回数据列表
    def get_data_from_slave(self):
        read_code = self.read()

        if not self.content:
            return []
        
        if read_code and self.check_digit_ok == self.check_digit_user:
            valid_data = self.content
            self.content = []
            return valid_data
        return []
    
    # 根据下位机返回数据列表解包单个数据
    def get_single_data_from_slave(self, id, command):
        if id == StepperMotorType.STEPPER_MOTOR_42.value:
            self.control_command(DeviceAdress.STEPPER_MOTOR_42.value, command)
        elif id == StepperMotorType.STEPPER_MOTOR_57.value:
            self.control_command(DeviceAdress.STEPPER_MOTOR_57.value, command)

        valid_data = self.get_data_from_slave()
        if len(valid_data) == 1:
            return valid_data[0]
        return self.invalid_data


    # 解包用户输入数据
    def unpack_args(self, *args):
        bits_pack_list = []
        args_list = list(args)
        for args in args_list:
            pair = struct.pack('>h', args)
            if len(pair) == 2:
                bits_pack_list.append(pair[0])
                bits_pack_list.append(pair[1])
            else:
                bits_pack_list = []
        return bits_pack_list

    # 用户控制指令数据处理
    def control_command(self, adress, command, *args):
        unpack_list = self.unpack_args(*args)
        if DEBUG == True:
            print("unpack_list: ", unpack_list)

        new_data_buff = unpack_list
        if DEBUG == True:
            print("adress: ", adress)
            print("command: ", command)
            print("new_data_buff len: ", len(new_data_buff))
            print("new_data_buff: ", new_data_buff)

        if (adress == DeviceAdress.STEPPER_MOTOR_42.value or adress == DeviceAdress.STEPPER_MOTOR_57.value) \
            and (command == Command.SET_DIR.value or command == Command.SET_SPEED.value):
            new_data_buff.pop(0)

        if (adress == DeviceAdress.STEPPER_MOTOR_42.value or adress == DeviceAdress.STEPPER_MOTOR_57.value) \
            and (command == Command.WRITE_ANGLE.value):
            new_data_buff.pop(2)

        if (adress == DeviceAdress.STEPPER_MOTOR_42.value or adress == DeviceAdress.STEPPER_MOTOR_57.value) \
            and (command == Command.WRITE_STEPS.value):
            new_data_buff.pop(2)
            new_data_buff.pop(3)

        if (adress == DeviceAdress.STEPPER_MOTOR_57.value) and (command == Command.WRITE_STEPS_BY_SWITCH.value):
            new_data_buff.pop(0)
            new_data_buff.pop(1)

        if (adress == DeviceAdress.STEPPER_MOTOR_42.value) and (command == Command.WRITE_DISTANCE.value):
            new_data_buff.pop(2)
            new_data_buff.pop(3)

        if (adress == DeviceAdress.STEPPER_MOTOR_42.value) and (command == Command.WRITE_DISTANCE_ZERO.value):
            new_data_buff.pop(0)
        if DEBUG == True:
            print("new_data_buff: ", new_data_buff)

        if self.invalid_data < len(new_data_buff):
            self.write(adress, new_data_buff, command)


    # 速度范围检查
    def speed_range_check(self, speed, min=0, max=100):
        return min <= speed <= max

    # 方向范围检查
    def dir_range_check(self, dir):
        return dir == MotorDirection.CLOCKWISE.value or dir == MotorDirection.COUNTCLOCKWISE.value
    

    # 获取TOF距离（只对奥创机械臂传送带套装有效）
    def get_tof_distance(self):
        self.control_command(DeviceAdress.IR_DETECT.value, Command.GET_TOF_DISTANCE.value)

        distance = -1
        valid_data = self.get_data_from_slave()
        data_len = len(valid_data)
        if data_len > 0:
            if data_len == 1:
                distance = valid_data[0]
            elif data_len == 2:
                distance = (valid_data[0] << 8) | valid_data[1]
        if 20 <= distance:
            return distance
        return -1
    
    # 根据开关控制步进电机传送带（只对奥创机械臂传送带套装有效）
    def control_conveyor_by_switch(self, swicth, speed):
        if self.speed_range_check(speed) and (swicth == SwitchMode.CLOSE.value or swicth == SwitchMode.OPEN.value):
            self.control_command(DeviceAdress.STEPPER_MOTOR_57.value, Command.WRITE_STEPS_BY_SWITCH.value, swicth, speed)

    # 步进电机传送带打开（只对奥创机械臂传送带套装有效）
    def open_conveyor(self, speed):
        if self.speed_range_check(speed):
            self.control_conveyor_by_switch(SwitchMode.OPEN.value, speed)

    # 步进电机传送带关闭（只对奥创机械臂传送带套装有效）
    def close_conveyor(self):
        self.control_conveyor_by_switch(SwitchMode.CLOSE.value, 0)


    # 获取当前滑轨移动距离（只对奥创机械臂滑轨套装有效）
    def get_distance(self):
        return self.get_single_data_from_slave(StepperMotorType.STEPPER_MOTOR_42.value, Command.GET_DISTANCE.value)
    
    # 根据托盘直径设置滑轨移动距离（只对奥创机械臂滑轨套装有效）
    def write_distance(self, distance, speed, tray_diameter_cm):
        if self.speed_range_check(speed) and (1 <= distance <= 10):
            self.control_command(DeviceAdress.STEPPER_MOTOR_42.value, Command.WRITE_DISTANCE.value, distance, speed, tray_diameter_cm)

    # 回零位（只对奥创机械臂滑轨套装有效）
    def move_zero(self, speed):
        if self.speed_range_check(speed):
            self.control_command(DeviceAdress.STEPPER_MOTOR_42.value, Command.WRITE_DISTANCE_ZERO.value, speed)
    

    # 获取电机方向（奥创机械臂滑轨、传送带套装有效）
    def get_dir(self, id):
        return self.get_single_data_from_slave(id, Command.GET_DIR.value)

    # 设置电机方向（奥创机械臂滑轨、传送带套装有效）
    def set_dir(self, id, dir):
        if self.dir_range_check(dir):
            if id == StepperMotorType.STEPPER_MOTOR_42.value:
                self.control_command(DeviceAdress.STEPPER_MOTOR_42.value, Command.SET_DIR.value, dir)
            elif id == StepperMotorType.STEPPER_MOTOR_57.value:
                self.control_command(DeviceAdress.STEPPER_MOTOR_57.value, Command.SET_DIR.value, dir)

    # 获取电机速度（奥创机械臂滑轨、传送带套装有效）
    def get_speed(self, id):
        return self.get_single_data_from_slave(id, Command.GET_SPEED.value)
    
    # 设置电机速度（奥创机械臂滑轨、传送带套装有效）
    def set_speed(self, id, speed):
        if self.speed_range_check(speed):
            if id == StepperMotorType.STEPPER_MOTOR_42.value:
                self.control_command(DeviceAdress.STEPPER_MOTOR_42.value, Command.SET_SPEED.value, speed)
            elif id == StepperMotorType.STEPPER_MOTOR_57.value:
                self.control_command(DeviceAdress.STEPPER_MOTOR_57.value, Command.SET_SPEED.value, speed)

    # 设置电机角度（奥创机械臂滑轨、传送带套装有效）
    def write_angle(self, id, angle, speed):
        if self.speed_range_check(speed):
            if id == StepperMotorType.STEPPER_MOTOR_42.value:
                self.control_command(DeviceAdress.STEPPER_MOTOR_42.value, Command.WRITE_ANGLE.value, angle, speed)
            elif id == StepperMotorType.STEPPER_MOTOR_57.value:
                self.control_command(DeviceAdress.STEPPER_MOTOR_57.value, Command.WRITE_ANGLE.value, angle, speed)

    # 根据步进数控制电机（奥创机械臂滑轨、传送带套装有效）
    def write_steps(self, id, steps, speed, dir):
        if steps > 0 and self.speed_range_check(speed) and self.dir_range_check(dir):
            if id == StepperMotorType.STEPPER_MOTOR_42.value:
                self.control_command(DeviceAdress.STEPPER_MOTOR_42.value, Command.WRITE_STEPS.value, steps, speed, dir)
            elif id == StepperMotorType.STEPPER_MOTOR_57.value:
                self.control_command(DeviceAdress.STEPPER_MOTOR_57.value, Command.WRITE_STEPS.value, steps, speed, dir)