#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int8MultiArray # this is the same as Bump right?
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
        self.ang_vel = 4
        self.side_started = False
        self.turn_started = False
    
    def odom_callback(self, msg):
        pos = msg.pose.pose.position
        orient = msg.pose.pose.orientation
        orientation_tuple = (orient.x, orient.y, orient.z, orient.w)
        angles = euler_from_quaternion(orientation_tuple)
        self.heading = angles[2]
        self.x = pos.x
        self.y = pos.y
        
    def square_side(self):

        if not self.side_started:
            self.targ_x = abs(self.x) + 1
            self.side_started = True

        #print(self.targ_x)


        self.pub.publish(Twist(linear=Vector3(x=self.vel, y=0)))

    def corner_turn(self):
        if not self.turn_started:
            self.targ_heading = self.heading + math.pi/2
            self.turn_started = True

        #print(self.targ_heading)

        self.pub.publish(Twist(angular=Vector3(z=self.ang_vel)))

    def run(self):
        while not rospy.is_shutdown():
            time.sleep(2)
            print("----------")
            print("x_pos:" + str(self.x) + " x_targ:" + str(self.targ_x))
            print("neato_ang:" + str(self.heading) + " ang_targ:" + str(self.targ_x))

            self.square_side()

            if(abs(round(self.x, 2)) >= abs(round(self.targ_x, 2))):
                self.pub.publish(Twist(linear=Vector3(x=0, y=0)))

                self.corner_turn()

                if(round(self.heading, 2) >= round(self.targ_heading, 2)):
                    self.pub.publish(Twist(angular=Vector3(z=0)))


if __name__ == '__main__':
    ds = DriveSquare()
    ds.run()

    #TODO WE MIGHT BE USING ODOM DATA INCORRECTLY (probably should be in world coord not neato)
