#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int8MultiArray
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import PointStamped
from tf.transformations import euler_from_quaternion, rotation_matrix, quaternion_from_matrix
import math
import time

class PersonFollower():
    def __init__(self):
        rospy.init_node('person_follower')
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('/scan', Twist, self.process_scan)
        # rospy.Subscriber("/my_point", PointStamped, process_point)
        self.neato_state = None
        self.theta = None
        self.ang_vel = 0.2
        self.linear_vel = .15
        self.lidar_range = []
        self.lidar_scan = []

    def process_scan(self, msg):
        self.lidar_scan = msg.ranges
        for i in range (0,361):
            print("lidar val: " + str(self.lidar_scan[i]))
            print("i: " + str(i))
            if (self.lidar_scan[i] < 2):
                self.lidar_range.append(i)
                # print("lidar val: " + str(self.lidar_scan[i]))

    # def calc_center_mass(self):
    #     self.heading = len(self.lidar_range) / 2
    #     print("Heading: " + str(self.heading))

    def run(self):
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            time.sleep(1)
            print("Still alive")
            # self.calc_center_mass()
            r.sleep()

if __name__ == '__main__':
    w = PersonFollower()
    w.run()



