#!/usr/bin/python3.5

from cfrankr import Affine, Gripper, MotionData, Robot, Waypoint  # pylint: disable=E0611
from multiprocessing import Process
from subprocess import Popen
import sys
import time
from typing import List, Optional
#from utils.camera import Camera
import matplotlib.pyplot as plt 
import tensorflow as tf 
import numpy as np
import cv2 
from cv_bridge import CvBridge, CvBridgeError
from cv_bridge.boost.cv_bridge_boost import getCvType



#############################################
# subscribe to realsense node and get image #
#############################################
import rospkg
import rospy
from sensor_msgs.msg import CameraInfo
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage

#import pyrealsense2 as rs

def pyreal():
    # Create a context object. This object owns the handles to all connected realsense devices
    pipeline = rs.pipeline()
    pipeline.start()

    try:
        while True:
            # Create a pipeline object. This object configures the streaming camera and owns it's handle
            frames = pipeline.wait_for_frames()
            depth = frames.get_depth_frame()
            if not depth: continue

            # Print a simple text-based representation of the image, by breaking it into 10x20 pixel regions and approximating the coverage of pixels within one meter
            coverage = [0]*64
            for y in xrange(480):
                for x in xrange(640):
                    dist = depth.get_distance(x, y)
                    if 0 < dist and dist < 1:
                        coverage[x/10] += 1

                if y%20 is 19:
                    line = ""
                    for c in coverage:
                        line += " .:nhBXWW"[c/25]
                    coverage = [0]*64
                    print(line)

    finally:
        pipeline.stop()

    depth = frames.get_depth_frame()
    depth_data = depth.as_frame().get_data()
    np_image = np.asanyarray(depth_data)

    return np_image

def callback(img):
    print("test")
    print(img.encoding) # 16UC1
    print(img.height) # 480
    print(img.width) # 640

    bridge = CvBridge()
    
    try:
        cv_image = bridge.imgmsg_to_cv2(img, img.encoding)
        
        (rows,cols) = cv_image.shape
        if cols > 60 and rows > 60 :
            cv2.circle(cv_image, (50,50), 10, 255)
            
            #cv2.imshow("Image window", cv_image)
            #cv2.waitKey(3)
            plt.imshow(cv_image)
            plt.show()

    except CvBridgeError as e:
        print(e)
    
    #plt.imshow(cv_image)
    #plt.show()
    #rospy.loginfo(rospy.get_caller_id(), img)

def cameraListener():
    rospy.init_node('cameraListener', anonymous=True)
    rospy.Subscriber('/camera/depth/image_rect_raw', Image, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':

    cameraListener()

# Can you train model on one photo?? No 
# How to use the livestream as dataset ... 




#camera = Camera(camera_suffixes='rc')
#image = camera.take_images()

#for l in image:
#    plt.imshow(image[l])
#    plt.show()



#gripper = Gripper('10.224.60.160', 0.06, 40.0)
#robot = Robot('panda_arm', 0.32)
#frame = Affine()

#pose = robot.current_pose(frame)

#print(pose)
#gripper.homing()
