#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int8MultiArray
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import PointStamped
from tf.transformations import euler_from_quaternion, rotation_matrix, quaternion_from_matrix
import math
import time
import numpy as np

class PersonFollower():
    def __init__(self):
        rospy.init_node('person_follower')
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('/scan', LaserScan, self.process_scan)
        self.neato_state = None
        self.theta = None
        self.ang_vel = 0.2
        self.linear_vel = .15
        self.lidar_range_index = []
        self.lidar_range_values = []
        self.lidar_scan = []
        self.targ_heading = None
        self.turn = True

    def process_scan(self, msg):
        self.lidar_scan = msg.ranges
        self.lidar_range_index = []
        self.lidar_range_values = []
        for i in range(0,361):
            if np.isinf(self.lidar_scan[i]) == False:
                self.lidar_range_values.append(self.lidar_scan[i])
                self.lidar_range_index.append(i)
        list_index = np.argmin(self.lidar_range_values)
        self.targ_heading = self.lidar_range_index[list_index]
        print(self.targ_heading)

    def controller(self):
        ang_vel = 0.004 * self.targ_heading
        self.pub.publish(Twist(angular=Vector3(z=ang_vel)))

    def pursue_person(self):
        if self.turn == True:
            self.controller()
        if 355 < self.targ_heading < 5:
            self.pub.publish(Twist(angular=Vector3(z=0)))
            self.turn = False




    # def calc_center_mass(self):
    #     self.heading = len(self.lidar_range) / 2
    #     print("Heading: " + str(self.heading))

    def run(self):
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            time.sleep(1)
            self.pursue_person()
            r.sleep()

if __name__ == '__main__':
    w = PersonFollower()
    w.run()



