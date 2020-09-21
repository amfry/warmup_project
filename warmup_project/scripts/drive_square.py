#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int8MultiArray # this is the same as Bump right?
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, rotation_matrix, quaternion_from_matrix
import time
from geometry_msgs.msg import Twist, Vector3

class DriveSquare():
    def __init__(self):
        rospy.init_node('drive_square')
        # TODO add publisher
        rospy.Subscriber('/odom', Odometry, self.odomCallback)
        self.heading = None
        self.x = None
        self.y = None
    
    def odomCallback(self, msg):
        pos = msg.pose.pose.position
        orient = msg.pose.pose.orientation
        orientation_tuple = (orient.x, orient.y, orient.z, orient.w)
        angles = euler_from_quaternion(orientation_tuple)
        self.heading = angles[2]
        self.x = pos.x
        self.y = pos.y

    def run(self):
        while not rospy.is_shutdown():
            print("x_pos:" + str(ds.x))
            print("y_pos:" + str(ds.y))
            print("neato_ang:" + str(ds.heading))


if __name__ == '__main__':
    ds = DriveSquare()
    ds.run()
