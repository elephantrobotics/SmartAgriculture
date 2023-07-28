from R1Control.MechArmController import MechArmController
from ConveyorControl.ConveyorMain import ConveyorMain
from R1Control.TcpClient import TcpClient
from R1Control.Common import *
import numpy as np
import time
import logging
import concurrent.futures


class RobotR1(MechArmController):
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

    def conveyor_belt_check(self):
        # 关闭传送带
        self.conveyor.close_conveyor()
        time.sleep(1)

    def __init__(
        self,
        client_handle,
        robot_port: str,
        conveyor_port: str,
        robot_baud: int = 115200,
        conveyor_baud: int = 115200,
    ):
        super().__init__(robot_port, robot_baud)
        self.robot_restore_point1     = [-87.97, -25.4, -21.26, 0, 49.74, 0]  # 机械臂初始恢复角1
        self.robot_restore_point2     = [5.71, -24.43, -21.26, 0, 49.74, 0]   # 机械臂初始恢复角2
        self.robot_initial_pose       = [-86.66, -40.69, -9.58, 0, 55.37, 0]  # 机械臂初始姿态角

        # old: [4.13, 14.67, -23.29, 79.71, 82.35, 0]
        # new: [2.02, 39.9, 11.68, 86.04, 85.86, 0]
        # self.robot_precatch_pose      = [2.0, 39.9, 11.68, 86.04, 85.86, 0]   # 机械臂抓取前初始预姿态角
        self.robot_precatch_pose      = [2.19, 35.13, 2.46, 89.2, 95.35, 10.81]   # 机械臂抓取前初始预姿态角

        self.conveyor_waiting_point   = [-6.0, -30.58, -36.65, 0, 84.81, 0]   # 传送带等待点
        self.conveyor_entry_point     = [-89.0, -30.67, -36.65, 0, 84.81, 0]  # 传送带进入点
        self.conveyor_placement_point = [-89.0, 16.42, -34.89, 0, 77.34, 0]   # 传送带放置点
        self.conveyor_restore_point   = [-89.0, -12.74, -47.37, 0, 63.01, 0]  # 传送带恢复点

        self.camera_coord             = np.array([0.0, 0.0, 0.0])   # 相机到目标的实时坐标点
        self.camera_pos               = np.array([85,-90.5,180])  # 相机相对于机械臂的固定坐标
        self.end_coords               = np.array([0.0, 0.0, 0.0])   # 根据相机坐标转换后目标的实际坐标

        self.old_camera_coord_list    = []  # 上一次相机实时坐标列表

        self.recheck_times = 0  # 重新检测摘取的次数

        self.client = client_handle

        self.conveyor                 = ConveyorMain(conveyor_port, conveyor_baud)  # 传送带控制对象

        self.robot_check()
        self.conveyor_belt_check()


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
            [-self.camera_coord[0], self.camera_coord[2], -self.camera_coord[1]]
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
        self.ma.send_angles(self.robot_restore_point1, speed)
        time.sleep(delay)
        self.ma.send_angles(self.robot_restore_point2, speed)
        time.sleep(delay)

    # 摘取前姿态预调整
    def pickup_attitude_adjustment_action(self, speed, delay):
        self.ma.send_angles(self.robot_precatch_pose, speed)
        time.sleep(delay)

    # 摘取等待点坐标
    def waiting_point_action(self, waiting_coords, x_pattern, x, y_pattern, y, z_pattern, z, speed):
        new_coords = self.spatial_adjustment(waiting_coords, x_pattern, x, y_pattern, y, z_pattern, z)
        self.ma.send_coords(new_coords, speed)
        time.sleep(3)

        a_waiting_point = self.reacquire_get_angles()
        time.sleep(5)
        # a_waiting_point[self.Joints.J6.value] -= 100
        a_waiting_point[self.Joints.J6.value] -= 58
        self.ma.send_angles(a_waiting_point,70)
        time.sleep(3) #5
        # self.ma.send_angle(6,-58, 70)
        # time.sleep(5)
        self.set_gripper_range(35, 70)
        time.sleep(5)
        gripper_value = self.ma.get_gripper_value()
        time.sleep(2)
        while gripper_value <= 30 or 40 <= gripper_value:
            self.set_gripper_range(35, 70)
            time.sleep(5)
            gripper_value = self.ma.get_gripper_value()
        return self.reacquire_get_coords()

    # 摘取实际点动作
    def pickup_point_action(self, entry_coords, x_pattern, x, y_pattern, y, z_pattern, z, speed):
        self.ma.send_coords(self.spatial_adjustment(entry_coords, x_pattern, x, y_pattern, y, z_pattern, z), speed)
        time.sleep(3)

        # 关闭夹爪摘取果子
        # self.set_gripper_range(3, 70)
        self.set_gripper_range(3, 70)
        # self.gripper_close()
        # time.sleep(5)
        self.set_gripper_range(0, 70)
        time.sleep(3)
        while 10 <= self.ma.get_gripper_value() or self.ma.get_gripper_value() < 0:
            self.set_gripper_range(0, 70)
            time.sleep(3)

        # 摘取完果子临时插补点，防止撞到没摘的果子
        self.ma.send_coords(self.spatial_adjustment(self.reacquire_get_coords(), x_pattern, 0.0, '-', 50, '+', 10), speed)
        time.sleep(3)

    # 将果子运输至传送带上方
    def transport_to_conveyor_track_point_action(self, speed, delay):
        # 移动到传送带上方轨迹前等待点（防止撞到3D摄像头）
        self.ma.send_angles(self.conveyor_waiting_point, speed)
        time.sleep(delay)
        
        # 移动到传送带上方
        self.ma.send_angles(self.conveyor_entry_point, speed)
        time.sleep(delay)

    # 放置果子动作
    def placement_action(self, speed, delay):
        # 下放至传送带轨迹
        self.ma.send_angles(self.conveyor_placement_point, speed)
        time.sleep(delay)

        # 张开夹爪放置果子
        # self.set_gripper_range(50)
        # self.set_gripper_range(50)

        self.set_gripper_range(40, 70)
        time.sleep(5)
        gripper_value = self.ma.get_gripper_value()
        time.sleep(2)
        while gripper_value <= 35 or 45 <= gripper_value:
            self.set_gripper_range(40, 70)
            time.sleep(5)
            gripper_value = self.ma.get_gripper_value()

        # 上调至传送带轨迹
        self.ma.send_angles(self.conveyor_restore_point, 25)
        time.sleep(delay)

        self.gripper_close()
        time.sleep(delay)

    # 控制传送带移动到摄像头位置
    def conveyor_ctl_to_camera_tarpoint_action(self):
        # 先让果子放置平稳
        time.sleep(3)

        #开启传送带
        self.conveyor.open_conveyor(1)
        time.sleep(1.25)
        # if 

        #关闭传送带
        self.conveyor.close_conveyor()

    # 摘取果子轨迹规划
    def trajectory_plan(self, cap_thread, speed, delay):
        flag = False
        # print(self.client.get_current_extracted_count())
        if DEBUG:
            with open("log.txt", "a") as f:
                f.write("self.client.get_current_extracted_count(): "+str(self.client.get_current_extracted_count())+ "\n")
        if self.client.get_current_extracted_count() == 0:
            print(self.old_camera_coord_list)
            if DEBUG:
                with open("log.txt", "a") as f:
                    f.write( "R1: "+ str(self.old_camera_coord_list)+ "\n")
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
                        c_entry_point = self.waiting_point_action(c_waiting_point, '-', 10, '-', 50.0, '+', 15.0, 40)
                        logging.info(f"Entry coords: {c_entry_point}")
                        
                        # 摘取实际点动作
                        self.pickup_point_action(c_entry_point, '-', 0, '+', 60, '+', 15, 60)
                        # if camera_coord[0] < -40 and camera_coord[1] > 50:
                        #     self.pickup_point_action(c_entry_point, '+', 10.0, '+', 60, '-', 1.0, 20)
                        # elif camera_coord[0] > 40 and camera_coord[1] < -30:
                        #     self.pickup_point_action(c_entry_point, '+', 5.0, '+', 55, '+', 6.0, 20)
                        # else:
                        #     self.pickup_point_action(c_entry_point, '+', 2.0, '+', 60, '-', 1.0, 20)

                        # 传送带轨迹规划动作
                        self.transport_to_conveyor_track_point_action(speed, delay)

                        # 放置果子动作
                        self.placement_action(speed, delay)
                        
                        # 摄像头轨迹规划动作
                        self.conveyor_ctl_to_camera_tarpoint_action()

                        flag = True
        if flag and cap_thread.is_apple() == False:
            self.client.set_current_extracted_count()
            print("\n\n\n\n")
            print(1)
            print(1)
            print(1)
            print(1)
            self.client.send_data("1")
            print(1)
            print(1)
            print(1)
            print(1)
            
        return flag


    def motion(self, cap_thread, speed=default_speed, delay=default_delay):
        # 超过100次没检测到好果则设置摘取坏果范围
        print("R1:", self.recheck_times)
        if DEBUG:
            with open("log.txt", "a") as f:
                f.write("self.recheck_times: "+str(self.recheck_times)+ "\n")
        # if self.recheck_times > 100:
        if self.recheck_times > 4:
            if cap_thread.is_apple() == True:
                cap_thread.set_detect_orange()
            else:
                cap_thread.set_detect_apple()
            self.recheck_times = 0

        # 没果子机械臂则回原点
        camera_coord_list = cap_thread.get_camera_coord_list()
        self.old_camera_coord_list = camera_coord_list
        camera_coord_list_len = len(self.old_camera_coord_list)
        if DEBUG:
            with open("log.txt", "a") as f:
                f.write("camera_coord_list_len: "+str(camera_coord_list_len)+ "\n")
        if camera_coord_list_len <= 0:
            self.move_start(speed, delay)
            if DEBUG:
                with open("log.txt", "a") as f:
                    f.write("motion: "+str(self.client.get_current_extracted_count())+ "\n")
            if self.client.get_current_extracted_count() == 0:
                self.recheck_times += 1
        else:
            try:
                action_end = self.trajectory_plan(cap_thread, speed, delay)
                # 只要是好果或坏果则满足条件
                # if self.client.get_server_notification() == True:
                #     # 服务器通知是好果就重新开启传送带
                #     if self.client.good_fruit():
                #         #重新开启传送带
                #         self.conveyor.open_conveyor(1)
                #         time.sleep(1.4)

                #         #关闭传送带
                #         self.conveyor.close_conveyor()
                if action_end and cap_thread.is_apple():
                    #重新开启传送带
                    time.sleep(2)
                    self.conveyor.open_conveyor(1)
                    time.sleep(2)

                    #关闭传送带
                    self.conveyor.close_conveyor()

                # 重置TCP缓存缓冲区
                self.client.reset_response_copy()
            except Exception as e:
                logging.error(f"Failed to execute motion: {e}")
        # self.trajectory_plan(speed, delay)


    # def trajectory_plan(self, speed, delay):
    #     flag = False
    #     for camera_coord in self.old_camera_coord_list:
    #         if camera_coord is not None:
    #             logging.info(f"Performing motion for camera coord: {camera_coord}")

    #             if len(camera_coord) == 3:
    #                 self.set_camera_coord(camera_coord[0], camera_coord[1], camera_coord[2])

    #                 # 摘取姿态调整，绕过摄像头
    #                 self.restore_postion_action(speed, delay)

    #                 # 摘取前姿态预调整
    #                 self.pickup_attitude_adjustment_action(speed, delay)

    #                 # 计算世界坐标
    #                 self.target_coords()
    #                 c_waiting_point = self.get_end_coords()
    #                 logging.info(f"Waiting coords: {c_waiting_point}")

    #                 # 摘取等待点动作
    #                 c_entry_point = self.waiting_point_action(c_waiting_point, '+', 9.0, '-', 46.0, '+', 17.0, 20)
    #                 logging.info(f"Entry coords: {c_entry_point}")

    #                 # 摘取实际点动作
    #                 self.pickup_point_action(c_entry_point, '+', 2.0, '+', 34.5, '+', 7.0, 20)

    #                 # 传送带轨迹规划动作
    #                 self.transport_to_conveyor_track_point_action(speed, delay)

    #                 # 放置果子动作
    #                 self.placement_action(speed, delay)

    #                 # 摄像头轨迹规划动作
    #                 self.conveyor_ctl_to_camera_tarpoint_action()

    #                 flag = True
    #                 break  # 优化: 执行完第一个摄像头坐标后立即结束循环

    #     if flag:
    #         self.client.set_current_extracted_count()

    #     return flag


    # def motion(self, cap_thread, speed=default_speed, delay=default_delay):
    #     # 超过100次没检测到好果则设置摘取坏果范围
    #     if self.recheck_times > 100:
    #         if cap_thread.is_apple():
    #             cap_thread.set_detect_orange()
    #         else:
    #             cap_thread.set_detect_apple()
    #         self.recheck_times = 0

    #     # 没果子机械臂则回原点
    #     camera_coord_list = cap_thread.get_camera_coord_list()
    #     self.old_camera_coord_list = camera_coord_list
    #     camera_coord_list_len = len(self.old_camera_coord_list)

    #     finish = False
    #     if camera_coord_list_len <= 0:
    #         self.move_start(speed, delay)
    #         self.recheck_times += 1
    #         return finish

    #     try:
    #         # 只要是好果或坏果则满足条件
    #         notification = self.client.get_server_notification()
    #         is_good_fruit = self.client.good_fruit()

    #         # 只有在获取到通知时才执行后续操作
    #         if notification:
    #             if is_good_fruit:
    #                 # 重新开启传送带
    #                 self.conveyor.open_conveyor(1)
    #                 time.sleep(1.4)
    #                 self.conveyor.close_conveyor()

    #             # 重置TCP缓存缓冲区
    #             self.client.reset_response_copy()

    #             # 并发执行trajectory_plan
    #             with concurrent.futures.ThreadPoolExecutor() as executor:
    #                 trajectory_future = executor.submit(self.trajectory_plan, speed, delay)

    #                 # 其他操作...
    #                 # ...

    #                 finish = trajectory_future.result()

    #     except Exception as e:
    #         logging.error(f"Failed to execute motion: {e}")

    #     return finish

