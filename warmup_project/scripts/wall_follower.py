#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int8MultiArray
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan
from tf.transformations import euler_from_quaternion, rotation_matrix, quaternion_from_matrix
import math
import time

class WallFollower():
    def __init__(self):
        rospy.init_node('wall_follower')
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('/scan', LaserScan, self.process_scan)
        self.L1 = 0
        self.L2 = 0
        self.H = 0
        self.neato_state = None
        self.theta = None
        self.ang_vel = 0.2
        self.linear_vel = .15

    def process_scan(self, msg):
        self.L1 = round(msg.ranges[225],1)
        self.L2 = round(msg.ranges[315],1)

        if self.L1 < self.L2:
            #print("Case 1")
            # Neato angle away from wall
            self.neato_state = 1
        if self.L1 > self.L2:
            #print("Case 2")
            # Neato angle towards wall
            self.neato_state = 2
        if self.L1 == self.L2:
            #print("Case 3")
            # Neato parallel to wall
            self.neato_state = 3

    def calc_heading(self):
        self.H = round(math.hypot(self.L1, self.L2),2)
        if self.neato_state == 1:
            #away
            print("case_1")
            alpha = math.degrees(math.asin(self.L1/self.H))
            self.theta = 45 - alpha
            # print("alpha: " + str(alpha))
            # print("angle: " + str(theta))
        if self.neato_state == 2:
            # towards
            print("case_2")
            beta = math.degrees(math.asin(self.L2 / self.H))
            self.theta = 45 - beta
            # print("alpha: " + str(alpha))
            # print("angle: " + str(theta))
        if self.neato_state == 3:
            #parallel
            print("case_3")
            self.theta = 0

    def controller(self):
        self.ang_vel = 0.005 * self.theta
        if self.neato_state == 1:
            self.pub.publish(Twist(angular=Vector3(z=-1*self.ang_vel)))
        if self.neato_state == 2:
            self.pub.publish(Twist(angular=Vector3(z=self.ang_vel)))


    def set_motion(self):
        self.calc_heading()
        if self.neato_state == 3:
            self.pub.publish(Twist(linear=Vector3(x=self.linear_vel, y=0)))
        if self.neato_state == 1 or self.neato_state == 2:
            self.controller()


    def run(self):
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            time.sleep(3)
            print("L1: " + str(self.L1))
            print("L2: " + str(self.L2))
            self.set_motion()
            r.sleep()

if __name__ == '__main__':
    w = WallFollower()
    w.run()



