#!/usr/bin/python3.5

import numpy as np
from cfrankr import Affine, Gripper, MotionData, Robot, Waypoint

bin_left_joint_values = [
            -1.8119446041276,
            1.1791089121678,
            1.7571002245448,
            -2.141621800118,
            -1.143369391372,
            1.633046061666,
            -0.432171664388
        ]
bin_right_joint_values = [
            -1.4637412426804,
            1.0494154046592,
            1.7926908288289,
            -2.283032105735,
            -1.035444400130,
            1.752863485400,
            0.04325164650034
        ]

general_dynamics_rel = 0.32

class Experiment():
    def __init__(self):

        self.robot = Robot('panda_arm', general_dynamics_rel)
        self.gripper = Gripper('10.224.60.160')

        self.md = MotionData().with_dynamics(1.0)


    # Test force mode
    def grasp(self): 
        md_approach_down = MotionData().with_dynamics(0.3).with_z_force_condition(20.0)  # dynamtics is both velocity and acceleration of robot (= 0.3)
        md_approach_up = MotionData().with_dynamics(1.0).with_z_force_condition(20.0)

        approach_distance_from_pose = 0.120
        action_approch_affine = Affine(z = approach_distance_from_pose)


        gripper_a = Affine(0.0, 0.0, 0.18, -np.pi / 4, 0.0, -np.pi)

        #robot.recover_from_errors()
        #gripper.homing()
        
        self.robot.move_relative_cartesian(gripper_a, action_approch_affine.inverse(), md_approach_down)
        self.robot.move_relative_cartesian(gripper_a, action_approch_affine, md_approach_up)

        self.robot.move_joints(bin_left_joint_values, self.md)
        self.robot.move_joints(bin_right_joint_values, self.md)
        self.robot.move_joints(bin_left_joint_values, self.md)

        if md_approach_down.did_break:
            self.robot.recover_from_errors()
            #action.collision = True
            self.robot.move_relative_cartesian(gripper_a, Affine(z=0.001), md_approach_up)


exp = Experiment()
exp.grasp()