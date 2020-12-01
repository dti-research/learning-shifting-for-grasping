#!/usr/bin/python3.5

from include/cfrankr import Affine, Gripper, MotionData, Robot, Waypoint  # pylint: disable=E0611
from multiprocessing import Process
from subprocess import Popen
import sys
import time
from typing import List, Optional



#gripper = Gripper('10.224.60.160', 0.06, 40.0)
robot = Robot('panda_arm', 0.32)
frame = Affine()

pose = robot.current_pose(frame)

print(pose)
#gripper.homing()
