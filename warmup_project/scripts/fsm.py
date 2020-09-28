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
        self.lidar_scan = None
        self.ang_vel = .55
        self.line_vel = .2
        self.state = self.drive_square()
        self.following_distance = 1

    def process_scan(self, msg):
        self.lidar_scan = msg.ranges
        for i in range(0, 361):
            if np.isinf(self.lidar_scan[i]) == False:
                self.lidar_range_values.append(self.lidar_scan[i])
                self.lidar_range_index.append(i)
        list_index = np.argmin(self.lidar_range_values)
        self.targ_heading = self.lidar_range_index[list_index]
        self.check_person()
        #print("targ_heading: "+str(self.targ_heading))
        print("person?: " + str(self.person_present))

    def check_person(self):
        for i in self.lidar_scan:
            if not np.isinf(i):
                self.person_present = True
                break
            else:
                self.person_present = False

    def drive_square(self):
        time.sleep(1)
        r = rospy.Rate(10)
        while not self.person_present:
            self.pub.publish(Twist(linear=Vector3(x=0, y=0), angular=Vector3(z=0)))
            self.pub.publish(Twist(linear=Vector3(x=self.line_vel, y=0)))
            time.sleep(5)
            self.pub.publish(Twist(linear=Vector3(x=0, y=0), angular=Vector3(z=self.ang_vel)))
            time.sleep(3)
            self.pub.publish(Twist(angular=Vector3(z=0)))
        while not rospy.is_shutdown():
            if self.person_present:
                self.pub.publish(Twist(linear=Vector3(x=0, y=0), angular=Vector3(z=0)))
                return self.follow_person
            r.sleep()

    def follow_person(self):
        r = rospy.Rate(10)
        #self.move_to_person()
        while not rospy.is_shutdown():
            print("step")
            if not self.person_present:
                return self.drive_square
            r.sleep

    # def move_to_person(self):
    #     if 3 < self.targ_heading < 357:
    #         self.angular_controller()
    #     else:
    #         self.pub.publish(Twist(angular=Vector3(z=0)))
    #         self.distance_follow()
    #
    # def angular_controller(self):
    #     ang_vel = 0.008 * self.targ_heading
    #     self.pub.publish(Twist(angular=Vector3(z=ang_vel)))
    #
    # def linear_controller(self):
    #     lin_vel = 0.2 * self.lidar_scan[0]
    #     self.pub.publish(Twist(linear=Vector3(x=lin_vel)))
    #
    # def distance_follow(self):
    #     print("distance: " + str(self.lidar_scan[0]))
    #     if self.lidar_scan[0] > self.following_distance:
    #         self.linear_controller()
    #     else:
    #         self.pub.publish(Twist(linear=Vector3(x=0)))


    def run(self):
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            self.state = self.state
            r.sleep()

if __name__ == '__main__':
    f = FiniteState()
    f.run()