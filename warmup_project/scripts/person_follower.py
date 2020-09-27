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
        self.following_distance = 1
        self.linear_vel = .15
        self.lidar_range_index = []
        self.lidar_range_values = []
        self.lidar_scan = []
        self.targ_heading = 0

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

    def angular_controller(self):
        ang_vel = 0.008 * self.targ_heading
        self.pub.publish(Twist(angular=Vector3(z=ang_vel)))
    
    def linear_controller(self):
        lin_vel = 0.2 * self.lidar_scan[0]
        self.pub.publish(Twist(linear=Vector3(x=lin_vel)))

    def distance_follow(self):
        print("distance: " + str(self.lidar_scan[0]))
        if self.lidar_scan[0] > self.following_distance:
            self.linear_controller()
            
        else:
            self.pub.publish(Twist(linear=Vector3(x=0)))

    def pursue_person(self):
        if 3 < self.targ_heading < 357:
            self.angular_controller()
        else:
            self.pub.publish(Twist(angular=Vector3(z=0)))
            self.distance_follow()

    def run(self):
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            time.sleep(1)
            self.pursue_person()
            r.sleep()

if __name__ == '__main__':
    w = PersonFollower()
    w.run()



