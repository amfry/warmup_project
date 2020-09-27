#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int8MultiArray
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan
from tf.transformations import euler_from_quaternion, rotation_matrix, quaternion_from_matrix
import math
import time

class PersonFollower():
    def __init__(self):
        rospy.init_node('person_follower')
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('/scan', LaserScan, self.process_scan)
        self.neato_state = None
        self.theta = None
        self.ang_vel = 0.2
        self.linear_vel = .15
        self.lidar_range = []

    def process_scan(self, msg):
        self.lidar_range = []
        for i in range (0,361):
            time.sleep(1)
            lidar = round(msg.ranges[i],1)
            print("lidar: " + str(lidar))

            if (lidar >= 2):
                self.lidar_range.append(i)
        self.calc_center_mass()

    def calc_center_mass(self):
        self.heading = len(self.lidar_range) / 2
        print("Heading: " + str(self.heading))

    def run(self):
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            time.sleep(1)
            print("Still alive")
            self.calc_center_mass()
            r.sleep()

if __name__ == '__main__':
    w = PersonFollower()
    w.run()



