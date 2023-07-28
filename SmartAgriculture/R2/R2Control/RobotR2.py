from R2Control.MechArmController import MechArmController
from R2Control.TcpServer import TcpServer
from R2Control.Common import *
import numpy as np
import time
import logging


class RobotR2(MechArmController):
    def status_check(self):
        # 检查270是否已上电，未上电则上电
        if not self.ma.is_power_on():
            self.ma.power_on()
            time.sleep(1)

        # 设置插补模式
        self.imputation_mode()
        time.sleep(1)

        # 夹爪合上
        self.gripper_close()
        time.sleep(1)

        # 根据夹爪实际直径比例设置当前工具坐标系范围
        self.ma.set_tool_reference([0, 0, flexible_jaw_diameter, 0, 0, 0])
        time.sleep(1)

        # 设置末端工具类型
        self.ma.set_end_type(1)
        time.sleep(1)

    def move_start(self, speed, delay):
        # 移动到初始姿态
        self.ma.send_angles(self.robot_initial_pose, speed)
        time.sleep(delay)

    def robot_check(self):
        self.status_check()
        self.move_start(default_speed, 3)


    def __init__(
        self,
        server_handle,
        robot_port: str,
        robot_baud: int = 115200,
    ):
        super().__init__(robot_port, robot_baud)
        self.server = server_handle  # Tcp服务端

        # self.robot_initial_pose  = [-79.89, -21.26, -5.71, -0.08, 98.78, -0.61] # 机械臂初始姿态角
        self.robot_initial_pose = [-90, -35.33, 0.52, -3.77, 99.05, 0.08]
        # self.robot_precatch_pose = [-0.43, -21.26, -5.88, 1.31, 98.78, -1.66]  # 机械臂抓取前初始预姿态角
        self.robot_precatch_pose = [-0.43, -35.33, 0.52, -3.77, 99.05, 0.08]
        # self.conveyor_waiting_point = [-6.0, -30.58, -36.65, 0, 84.81, 0]   # 传送带等待点
        # self.conveyor_entry_point   = [-89.0, -30.67, -36.65, 0, 84.81, 0]  # 传送带进入点
        self.box_waiting_point = [-90, -9.4, -14.23, -0.17, 83.75, 0.35]
        self.box_entry_point = [-94.04, 20.74, -9.58, 2.81, 59.86, 0.26]
        self.camera_coord          = np.array([0.0, 0.0, 0.0])        # 相机到目标的实时坐标点
        # self.camera_pos            = np.array([144, -18, 370])  # 相机到目标的固定坐标点
        self.camera_pos            = np.array([130, -14, 376])
        self.end_coords            = np.array([0.0, 0.0, 0.0])        # 根据相机坐标转换后的实际世界坐标点
        self.old_camera_coord_list = []                               # 上一次相机实时坐标列表
        self.robot_check()
        self.nothing_count = 0

    # 获取真实相机世界坐标x, y, z
    def get_camera_coord(self):
        return self.camera_coord
    
    # 设置真实相机世界坐标x, y, z
    def set_camera_coord(self, x: float, y: float, z: float):
        self.camera_coord = np.array([x, y, z])

    # 获取转换后机械臂可以运动的世界坐标
    def get_end_coords(self):
        return self.end_coords

    # 辅助计算机械臂可移动坐标
    def model_track(self):
        model_pos = np.array(
            [self.camera_coord[1], -self.camera_coord[0], -self.camera_coord[2]]
        )
        target_pos = model_pos + self.camera_pos

        if DEBUG == True:
            print("model_pos: ", model_pos)
            print("target_pos: ", target_pos)

        return target_pos

    #根据相机真实坐标计算机械臂实际可移动世界坐标
    def target_coords(self):
        coord = self.ma.get_coords()
        while len(coord) == 0:
            coord = self.ma.get_coords()

        target = self.model_track()
        coord[:3] = target.copy()
        self.end_coords = coord[:3]

        if DEBUG == True:
            print("coord: ", coord)
            print("self.end_coords: ", self.end_coords)

        # 更新实际转换的世界坐标系
        self.end_coords = coord

        return coord

    # 摘取前位置调整，避免档到3D摄像头
    def restore_postion_action(self, speed, delay):
        self.ma.send_angles(self.robot_initial_pose, speed)
        time.sleep(delay)

    # 摘取前姿态预调整
    def pickup_attitude_adjustment_action(self, speed, delay):
        self.ma.send_angles(self.robot_precatch_pose, 50)
        time.sleep(delay)

    # 摘取等待点坐标
    def waiting_point_action(self, waiting_coords, x_pattern, x, y_pattern, y, z_pattern, z, speed):
        new_coords = self.spatial_adjustment(waiting_coords, x_pattern, x, y_pattern, y, z_pattern, z)
        # new_coords[1] -= 25
        # new_coords[0] -= 5
        # new_coords[2] -= 10
        self.ma.send_coords(new_coords, speed)
        time.sleep(3)

        self.set_gripper_range(50, 70)
        time.sleep(5)
        gripper_value = self.ma.get_gripper_value()
        time.sleep(2)
        while gripper_value <= 45 or 55 <= gripper_value:
            self.set_gripper_range(50, 70)
            time.sleep(5)
            gripper_value = self.ma.get_gripper_value()

        return self.reacquire_get_coords()

    # 摘取实际点动作
    def pickup_point_action(self, entry_coords, x_pattern, x, y_pattern, y, z_pattern, z, speed):
        self.ma.send_coords(self.spatial_adjustment(entry_coords, x_pattern, x, y_pattern, y, z_pattern, z), speed)
        time.sleep(3)

        # 关闭夹爪摘取果子
        
        
        self.set_gripper_range(0, 70)

        time.sleep(3)
        gripper_value = self.ma.get_gripper_value()
        time.sleep(2)
        if 10 <= gripper_value or gripper_value < 0:
            self.set_gripper_range(0, 70)
            time.sleep(3)
            gripper_value = self.ma.get_gripper_value()


        self.ma.send_angles(self.robot_precatch_pose,50)
        time.sleep(2)
        # # 摘取完果子临时插补点，防止撞到没摘的果子
        # self.ma.send_coords(self.spatial_adjustment(self.reacquire_get_coords(), '-', 0.0, '-', 0.0, '+', 30), speed)
        # time.sleep(3)
    # 放置果子动作
    def place_fruit(self, speed, delay):
        self.ma.send_angles(self.box_waiting_point, speed)
        time.sleep(delay)
        self.ma.send_angles(self.box_entry_point, speed)
        time.sleep(delay)
        self.set_gripper_range(40, 70)
        time.sleep(5)
        gripper_value = self.ma.get_gripper_value()
        time.sleep(2)
        if gripper_value <= 35 or 45 <= gripper_value:
            self.set_gripper_range(40, 70)
            time.sleep(5)
            gripper_value = self.ma.get_gripper_value()

        self.ma.send_angles(self.box_waiting_point, speed)
        time.sleep(delay)

        self.set_gripper_range(0, 70)

        time.sleep(3)
        gripper_value = self.ma.get_gripper_value()
        time.sleep(2)
        if 10 <= gripper_value or gripper_value < 0:
            self.set_gripper_range(0, 70)
            time.sleep(3)
            gripper_value = self.ma.get_gripper_value()


        

    # 摘取果子轨迹规划
    def trajectory_plan(self, fruit_type, speed, delay):
        if self.server.start_move:
            if DEBUG:
                with open("log.txt", "a") as f:
                    f.write( "R2: "+ str(self.old_camera_coord_list)+ "\n")
            for camera_coord in self.old_camera_coord_list:
                if camera_coord is not None:
                    logging.info(f"Performing motion for camera coord: {camera_coord}")

                    if len(camera_coord) == 3:
                        self.set_camera_coord(camera_coord[0], camera_coord[1], camera_coord[2])

                        # 摘取姿态调整，绕过摄像头
                        self.restore_postion_action(speed, delay)

                        # 摘取前姿态预调整
                        self.pickup_attitude_adjustment_action(speed, delay)
                        
                        # 计算世界坐标
                        self.target_coords()
                        c_waiting_point = self.get_end_coords()
                        logging.info(f"Waiting coords: {c_waiting_point}")

                        # 摘取等待点动作
                        # c_entry_point = self.waiting_point_action(c_waiting_point, '-', 19.5, '+', 27, '+', 30, 20)
                        # logging.info(f"Entry coords: {c_entry_point}")
                        c_entry_point = self.waiting_point_action(c_waiting_point, '-', 0, '+', 0, '+', 35, 50)
                        logging.info(f"Entry coords: {c_entry_point}")
                        # 摘取实际点动作
                        # self.pickup_point_action(c_entry_point, '-', 0.5, '-', 0.5, '-', 25.0, 20)
                        self.pickup_point_action(c_entry_point, '-', 0, '+', 0, '-', 40.0, 50)
                        # 放置果子
                        self.place_fruit(speed, delay)

                        # 证明果子已经不在识别区域
                        self.server.set_target(bad_fruit_str)
                        self.server.R2_action_done()
                else:
                    # 证明果子已经不在识别区域
                    # self.error_count += 1
                    
                    self.server.set_target(good_fruit_str)
                    break
            # if self.error_count >= 3:
            #     self.server.send_info("miss")

    def motion(self, camera_coord_list, fruit_type, speed=default_speed, delay=default_delay):
        self.old_camera_coord_list = camera_coord_list
        if DEBUG:
            with open("log.txt", "a") as f:
                f.write(" R2 :" + str(self.server.start_move)+str(self.old_camera_coord_list)+"\n")
        if self.server.start_move and (self.old_camera_coord_list == []):
            self.nothing_count += 1
        if self.nothing_count > 20:
            self.server.R2_action_done()
            self.nothing_count = 0
            if DEBUG:
                with open("log.txt", "a") as f:
                    f.write(" R2 detect falled ")
        # 没果子机械臂则回原点
        camera_coord_list_len = len(self.old_camera_coord_list)
        if camera_coord_list_len <= 0:
            self.move_start(speed, delay)
        else:
            try:
                self.trajectory_plan(fruit_type, speed, delay)
            except Exception as e:
                logging.error(f"Failed to execute motion: {e}")