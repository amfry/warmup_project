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

class FiniteState():
    def __init__(self):
        rospy.init_node('fsm')
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('/scan', LaserScan, self.process_scan)
        self.person_present = False
        self.targ_heading = 0
        self.lidar_range_index = [0]
        self.lidar_range_values = [0]
        self.lidar_scan = [0]
        self.ang_vel = .55
        self.line_vel = .2
        self.state = "square" # states are "square" and "person"
        self.following_distance = 1

    def process_scan(self, msg):
        self.lidar_scan = msg.ranges
        self.lidar_range_index = []
        self.lidar_range_values = []
        for i in range(0, 361):
            if np.isinf(self.lidar_scan[i]) == False:
                self.lidar_range_values.append(self.lidar_scan[i])
                self.lidar_range_index.append(i)
        if len(self.lidar_range_index) == 0:
            # self.angular_controller()
            self.person_present = False
        else:
            list_index = np.argmin(self.lidar_range_values)
            self.targ_heading = self.lidar_range_index[list_index]
            self.person_present = True
        # self.check_person()
        #print("person? " + str(self.person_present))
        #print(self.targ_heading)


    def check_person(self):
        for i in self.lidar_scan:
            if not np.isinf(i):
                self.person_present = True
                break
            else:
                self.person_present = False

    def move_to_person(self):
        self.pub.publish(Twist(linear=Vector3(x=0, y=0), angular=Vector3(z=0)))
        if 3 < self.targ_heading < 357:
            self.angular_controller()
        else:
            self.pub.publish(Twist(angular=Vector3(z=0)))
            self.distance_follow()
    
    def angular_controller(self):
        ang_vel = 0.015 * self.targ_heading
        self.pub.publish(Twist(angular=Vector3(z=ang_vel)))

    def linear_controller(self):
        if np.isinf(self.lidar_scan[0]):
            lin_vel = 0
        else:
            lin_vel = 0.2 * self.lidar_scan[0]
        self.pub.publish(Twist(linear=Vector3(x=lin_vel)))

    def distance_follow(self):
        print("distance: " + str(self.lidar_scan[0]))
        if self.lidar_scan[0] > self.following_distance:
            self.linear_controller()
        else:
            self.pub.publish(Twist(linear=Vector3(x=0)))

    def drive_square(self):
        self.line_vel = .2
        self.ang_vel = .55
        time.sleep(1)
        for i in range(0, 4):
            self.pub.publish(Twist(linear=Vector3(x=0, y=0), angular=Vector3(z=0)))
            self.pub.publish(Twist(linear=Vector3(x=self.line_vel, y=0)))
            time.sleep(5)
            self.pub.publish(Twist(linear=Vector3(x=0, y=0), angular=Vector3(z=self.ang_vel)))
            time.sleep(3)
            self.pub.publish(Twist(angular=Vector3(z=0)))

    def run(self):
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            if self.person_present:
                pass
                self.move_to_person()
            if not self.person_present:
                print("====== DRIVING SQUAREEEEEEEEEE ========")
                self.drive_square()
            r.sleep()

if __name__ == '__main__':
    f = FiniteState()
    f.run()
