#!/usr/bin/python
# Python 2/3 compatibility imports
from __future__ import print_function
from six.moves import input

import sys
import copy
import rospy
import numpy as np
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
#from config import Config
from cfrankr import Affine, Gripper, MotionData, Robot, Waypoint


# Initialize moveitcommander and rospy:
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial', anonymous=True)

# Instantiate a RobotCommander object which is the outer-level interfaceto the robot:
# robot = moveit_commander.RobotCommander()

# Instantiate a PlanningSceneInterface object which is an interface to theworld surrounding the robot:
scene = moveit_commander.PlanningSceneInterface()

# Instantiate a MoveGroupCommander object which is an interface to onegroup of joints:
group_name = "panda_arm"
move_group = moveit_commander.MoveGroupCommander(group_name)



# Test force mode 
md_approach_down = MotionData().with_dynamics(0.3).with_z_force_condition(7.0)  # dynamtics is both velocity and acceleration of robot (= 0.3)
approach_distance_from_pose = 0.120
general_dynamics_rel = 0.32
gripper = Affine(0.0, 0.0, 0.18, -np.pi / 4, 0.0, -np.pi)

action_approch_affine = Affine(z = approach_distance_from_pose)
robot = Robot('panda_arm', general_dynamics_rel)
robot.move_relative_cartesian(gripper, action_approch_affine.inverse(), md_approach_down)



joint_home = [0, -pi/4, 0, -3 * pi/4, 0, pi/2, pi/4]
joint_bin1 = [-0.0644031699864488, 0.32274379384726803, -0.10292667861152113, -1.2921963659378088, 0.05632472207445811, 1.6496457696122342, 0.6882092836954272]
joint_bin1 = [
            -1.8119446041276,
            1.1791089121678,
            1.7571002245448,
            -2.141621800118,
            -1.143369391372,
            1.633046061666,
            -0.432171664388
            ]
joint_bin2 = [0.12321019070998966, 0.34953718799875494, -0.009334989400345474, -1.2849881259302238, 0.03397058897170236, 1.67633656941519, 0.9283458901323183]

# pose_home = geometry_msgs.msg.Pose()
# pose_home.position.x = 0.306963803213
# pose_home.position.y = 0.000103313851
# pose_home.position.z = 0.590155468099
# pose_home.orientation.x = -0.924067128858
# pose_home.orientation.y = 0.382229388148
# pose_home.orientation.z = 0.000790639453278
# pose_home.orientation.w = 0.000230968503154

# pose_bin1 = geometry_msgs.msg.Pose()
# pose_bin1.position.x = 0.650364505733
# pose_bin1.position.y = -0.0933816632864
# pose_bin1.position.z = 0.569687031247
# pose_bin1.orientation.x = -0.910040850521
# pose_bin1.orientation.y = 0.413913317885
# pose_bin1.orientation.z = -0.015469283349
# pose_bin1.orientation.w = 0.0161900257551

# pose_bin2 = geometry_msgs.msg.Pose()
# pose_bin2.position.x = 0.661685800797
# pose_bin2.position.y = 0.0798241127199
# pose_bin2.position.z = 0.557067984371 
# pose_bin2.orientation.x = -0.917504858763
# pose_bin2.orientation.y = 0.396860155287
# pose_bin2.orientation.z = -0.0109796035031
# pose_bin2.orientation.w = 0.0237970502198


while True:
    # Move the robot to Home position via joint move
    move_group.go(joint_home, wait=True)
    move_group.stop()

    move_group.go(joint_bin1, wait=True)
    move_group.stop()

    move_group.go(joint_bin2, wait=True)
    move_group.stop()

# # pose move to bin 1
# move_group.set_pose_target(pose_bin1)
# move_group.go(wait=True)
# move_group.stop()
# move_group.clear_pose_targets()

# # pose move to bin 2
# move_group.set_pose_target(pose_bin2)
# move_group.go(wait=True)
# move_group.stop()
# move_group.clear_pose_targets()

# # Move the robot to Home position via joint move
# move_group.go(joint_home, wait=True)
# move_group.stop()

