#!/usr/bin/env python3

import tty
import select
import sys
import termios
import rospy
from geometry_msgs.msg import Vector3, Twist

class Teleop():
    def __init__(self):
        self.curr_key = None
        self.lin_vel = 0.2
        self.def_lin_vel = 0.1
        self.ang_vel = 8
        rospy.init_node('teleop')
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    def getKey(self):
        settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        key = sys.stdin.read(1)
        self.curr_key = key
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

    def setMotion(self):
        if self.curr_key == 'w':
            self.pub.publish(Twist(linear=Vector3(x=self.lin_vel)))
        if self.curr_key == 'p':
            self.pub.publish(Twist(linear=Vector3(x=0)))
        if self.curr_key == 's':
            self.pub.publish(Twist(linear=Vector3(x=-1 * self.lin_vel)))
        if self.curr_key == 'a':
            self.pub.publish(Twist(linear=(Vector3(x=0, y=0, z=0)), angular=Vector3(z=self.ang_vel)))
        if self.curr_key == 'd':
            self.pub.publish(Twist(linear=(Vector3(x=0, y=0, z=0)), angular=Vector3(z=-1 * self.ang_vel)))
        if self.curr_key == 'm':
            self.lin_vel += 0.1
            self.pub.publish(Twist(linear=Vector3(x=self.lin_vel)))
        if self.curr_key == 'n':
            self.lin_vel -= 0.1
            if self.lin_vel <= self.def_lin_vel:
                self.lin_vel = self.def_lin_vel
                self.pub.publish(Twist(linear=Vector3(x=self.lin_vel)))
            else:
                self.pub.publish(Twist(linear=Vector3(x=self.lin_vel)))

    def run(self):
        while self.curr_key != '\x03':
            self.getKey()
            self.setMotion()
            print(self.curr_key)
            rospy.Rate(10).sleep()
            
    
if __name__ == '__main__':
    t = Teleop()
    t.run()
