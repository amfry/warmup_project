#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int8MultiArray
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan
from tf.transformations import euler_from_quaternion, rotation_matrix, quaternion_from_matrix

class WallFollower():
    def __init__(self):
        rospy.init_node('wall_follower')
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('/scan', LaserScan, self.process_scan)
        self.L1 = None
        self.L2 = None

    def process_scan(self, msg):
        self.L1 = msg.ranges[0]
        # self.L2 = msg.ranges[315]

        print("L1: " + str(self.L1))
        # print("L2: " + str(self.L2))

        # if self.L1 > self.L2:
        #     print("Case 1")
        #     # Neato angle away from wall
        # if self.L1 < self.L2:
        #     print("Case 2")
        #     # Neato angle towards wall
        # if self.L1 == self.L2:
        #     print("Case 3")
        #     # Neato parallel to wall

    def run(self):
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            r.sleep()

if __name__ == '__main__':
    w = WallFollower()
    w.run()



