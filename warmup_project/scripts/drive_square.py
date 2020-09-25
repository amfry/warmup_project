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
        self.pos_reached = False
        self.angle_reached = False

        self.state = self.draw_line

    def odom_callback(self, msg):
        pos = msg.pose.pose.position
        orient = msg.pose.pose.orientation
        orientation_tuple = (orient.x, orient.y, orient.z, orient.w)
        angles = euler_from_quaternion(orientation_tuple)
        self.heading = angles[2]
        self.x = pos.x
        self.y = pos.y

    def calc_target_position(self):
        curr_x = self.x
        curr_y = self.y
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

    def calc_new_heading(self):
        curr_heading = self.heading
        temp_heading = curr_heading + .5*math.pi
        if temp_heading > math.pi:
            remainder = temp_heading % math.pi
            self.targ_heading = -1*math.pi + remainder
        else:
            self.targ_heading = temp_heading

    def monitor_heading(self):
        print("------Corner----------")
        head_comp = self.heading >= self.targ_heading
        print(head_comp)
        if head_comp:
            self.angle_reached = True
            print("NUT NUT NUT HEADINGGGG")
            print(self.angle_reached)
            self.pub.publish(Twist(angular=Vector3(z=0)))

    # def monitor_pos(self):
    #     print("heck ya")
    #     if round(self.x,1) >= round(self.targ_x,1) and round(self.y,1) >= round(self.targ_y,1):
    #             self.pub.publish(Twist(linear=Vector3(x=0, y=0)))
    #             self.pos_reached = True

    def monitor_pos(self):
        if (abs(self.y) < 0.5):
            y_comp = math.isclose(abs(self.y), abs(self.targ_y), abs_tol=.2)
        else:
            y_comp = math.isclose(self.y, self.targ_y, rel_tol=.2)
        if (abs(self.x) < 0.5):
            x_comp = math.isclose(abs(self.x), abs(self.targ_x), abs_tol=.2)
        else:
            x_comp = math.isclose(self.x, self.targ_x, rel_tol=.2)

        print("------Line----------")
        print(x_comp, y_comp)

        if x_comp and y_comp:
            self.pub.publish(Twist(linear=Vector3(x=0, y=0)))
            self.pos_reached = True

    def draw_line(self):
            r = rospy.Rate(10)
            self.calc_target_position()

            self.pub.publish(Twist(linear=Vector3(x=self.vel, y=0), angular=Vector3(z=0)))

            while not rospy.is_shutdown():
                self.monitor_pos()
                print("------------------")
                print("X pos: " + str(self.x))
                print("Y pos: " + str(self.y))
                print("X target: " + str(self.targ_x))
                print("Y target: " + str(self.targ_y))
                # print("Pos Reached: " + str(self.pos_reached))
                # print("")
                # print("")
                # print("Heading: " + str(self.heading))
                # print("Targ heading: " + str(self.y))
                # print("Angle Reached: " + str(self.angle_reached))
                # print("")
                # print("")
                time.sleep(1)
                if self.pos_reached:
                    print("Woop di doooo")
                    self.pos_reached = False
                    return self.turn_corner
                r.sleep()

    def turn_corner(self):
        r = rospy.Rate(10)
        self.calc_new_heading()

        self.pub.publish(Twist(angular=Vector3(z=self.ang_vel)))

        while not rospy.is_shutdown():
            self.monitor_heading()
            if self.angle_reached:
                self.angle_reached = False
                print("hello")
                return self.draw_line
            r.sleep()


    def run(self):
        rospy.sleep(1)
        while not rospy.is_shutdown():
            print("Pos flag: " + str(self.pos_reached))

            # print("Heading: " + str(self.heading))
            # print("Targ heading: " + str(self.y))
            # print("Angle Reached: " + str(self.angle_reached))

            self.state = self.state()
            print(self.state) #HELP doesn't print here

if __name__ == '__main__':
    ds = DriveSquare()
    ds.run()