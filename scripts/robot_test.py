#!/usr/bin/python3.5

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
