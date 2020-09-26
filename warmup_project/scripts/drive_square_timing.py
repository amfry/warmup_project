#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int8MultiArray
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, rotation_matrix, quaternion_from_matrix
import time
from geometry_msgs.msg import Twist, Vector3
import math

class DriveSquare():
    def __init__(self):
        rospy.init_node('drive_square')
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        self.line_vel = 0.2
        self.ang_vel = 0.55

    def run(self):
        time.sleep(1)
        for i in range (0,4):
            self.pub.publish(Twist(linear=Vector3(x=0, y=0), angular=Vector3(z=0)))
            self.pub.publish(Twist(linear=Vector3(x=self.line_vel, y=0)))
            time.sleep(5)
            self.pub.publish(Twist(linear=Vector3(x=0, y=0), angular=Vector3(z=self.ang_vel)))
            time.sleep(3)
            self.pub.publish(Twist(angular=Vector3(z=0)))

if __name__ == '__main__':
    ds = DriveSquare()
    ds.run()
