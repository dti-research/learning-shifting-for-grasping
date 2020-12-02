#!/usr/bin/python
# Python 2/3 compatibility imports
from __future__ import print_function
from six.moves import input

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list


moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial', anonymous=True)

group_name = "panda_arm"
move_group = moveit_commander.MoveGroupCommander(group_name)

current_pose = move_group.get_current_pose()
print("Current pose is: {}".format(current_pose))

current_joint_values = move_group.get_current_joint_values()()
print("Current joint values is: {}".format(current_joint_values))

