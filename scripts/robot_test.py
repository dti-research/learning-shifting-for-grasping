#!/usr/bin/python3.5

from cfrankr import Affine, Gripper, MotionData, Robot, Waypoint  # pylint: disable=E0611

gripper = Gripper('10.224.60.160', 0.06, 40.0)
robot = Robot('panda_arm', 0.32)

gripper.move(0.08)