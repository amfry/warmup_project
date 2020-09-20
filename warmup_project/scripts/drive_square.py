#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int8MultiArray # this is the same as Bump right?
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, Vector3 


class DriveSquare():
    def __init__(self):
        rospy.init_node('drive_square')
        # TODO add publisher
        rospy.Subscriber('/odom', Odometry, self.setSpeed)
    
    def setSpeed(self, msg): #TODO what is  msg
        print(msg.pose.pose)

if __name__ == '__main__':
    ds = DriveSquare()
    ds.setSpeed()
    