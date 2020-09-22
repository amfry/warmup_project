#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int8MultiArray  # this is the same as Bump right?
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, rotation_matrix, quaternion_from_matrix
import time
from geometry_msgs.msg import Twist, Vector3
import math


class DriveSquare():
    def __init__(self):
        rospy.init_node('drive_square')
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.heading = None
        self.x = None
        self.y = None
        self.targ_x = 0.0
        self.targ_y = 0.0
        self.targ_heading = 0.0
        self.vel = 0.2
        self.ang_vel = 0.2
        self.line_active = False
        self.corner_active = False

    def odom_callback(self, msg):
        pos = msg.pose.pose.position
        orient = msg.pose.pose.orientation
        orientation_tuple = (orient.x, orient.y, orient.z, orient.w)
        angles = euler_from_quaternion(orientation_tuple)
        self.heading = angles[2]
        self.x = pos.x
        self.y = pos.y

    def line(self):
        if not self.line_active:
            curr_x = self.x
            curr_y = self.y
            self.calc_target_position(curr_x, curr_y)
            self.pub.publish(Twist(linear=Vector3(x=self.vel, y=0)))
            self.line_active = True
        if self.line_active:
            if self.x >= self.targ_x:
                self.pub.publish(Twist(linear=Vector3(x=0, y=0)))
                self.line_active = False

    def calc_target_position(self, curr_x, curr_y):
        if 0 < self.heading <= .5 * math.pi:
            self.targ_x = math.cos(self.heading) + curr_x
            self.targ_y = math.sin(self.heading) + curr_y
        if math.pi*.5 < self.heading <= math.pi:
            self.targ_x = -1*math.cos(self.heading) + curr_x
            self.targ_y = math.sin(self.heading) + curr_y
        if math.pi*-.5 <= self.heading < 0:
            self.targ_x = math.cos(self.heading) + curr_x
            self.targ_y = -1*math.sin(self.heading) + curr_y
        if math.pi*-1 <= self.heading < -.5*math.pi:
            self.targ_x = -1*math.cos(self.heading) + curr_x
            self.targ_y = -1*math.sin(self.heading) + curr_y


    def corner(self):
        if not self.corner_active:
            curr_heading = self.heading
            temp_heading = curr_heading + .5*math.pi
            if temp_heading > math.pi:
                remainder = temp_heading % math.pi
                self.targ_heading = -1*math.pi + remainder
            else:
                self.targ_heading = temp_heading
            self.pub.publish(Twist(angular=Vector3(z=self.ang_vel)))
            self.corner_active = True
        if self.corner_active:
            if self.heading >= self.targ_heading:
                self.pub.publish(Twist(angular=Vector3(z=0)))
                self.corner_active = False


    def run(self):
        while not rospy.is_shutdown():
            time.sleep(2)
            print("----------")
            print("x_pos:" + str(self.x) + " x_targ:" + str(self.targ_x))
            print("neato_ang:" + str(self.heading) + " ang_targ:" + str(self.targ_x))
            if not self.corner_active:
                self.line()
            if not self.line_active:
                self.corner()

if __name__ == '__main__':
    ds = DriveSquare()
    ds.run()

    # TODO WE MIGHT BE USING ODOM DATA INCORRECTLY (probably should be in world coord not neato)
