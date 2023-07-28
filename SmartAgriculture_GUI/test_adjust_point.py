#!/usr/bin/python
# -*- coding:utf-8 -*-
# @File    : test_adjust_point.py
# @Author  : Wang Weijian
# @Time    :  2023/06/30 16:58:05
# @function: 用于270 M5 3D农业套装 R1 Robot机器抓取果子点位不准时，辅助调整点位的脚本，主要调整相机相对于机械臂的固定坐标（从左往右，以第一个相机镜头为准）--> self.camera_pos
# @version : V1

from pymycobot.mycobot import MyCobot
import time
from pymycobot.utils import get_port_list

plist = get_port_list()
print(plist)
mc = MyCobot(plist[1], 115200)
mc.set_tool_reference(([0, 0, 100, 0, 0, 0]))
mc.set_end_type(1)
time.sleep(1)
mc.release_all_servos()
time.sleep(2)

# [89.0, -93.1, 164.9, -96.74, -10.64, 179.59]
while 1:
    print(mc.get_coords())
    time.sleep(1.5)
