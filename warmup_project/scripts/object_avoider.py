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

class ObjectAvoider():
    def __init__(self):
        rospy.init_node('object_avoider')
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('/scan', LaserScan, self.process_scan)
        self.ang_vel = 0.3
        self.lin_vel = 0.2
        self.path_clear = None

    def process_scan(self, msg):
        self.lidar_scan = msg.ranges[0:20] + msg.ranges[340:360]
        print("Any: " + str(any(np.isinf(self.lidar_scan))))
        for i in self.lidar_scan:
            if i < 1:
                self.path_clear = False
                break
            else:
                self.path_clear = True
        propose_vel = min(self.lidar_scan) * 0.08
        if propose_vel * 0.08 > 1:
            self.lin_vel = .5
        else:
            self.lin_vel = propose_vel
        print("Lin vel: " + str(self.lin_vel))
        print("Clear? " + str(self.path_clear))
        print(self.lidar_scan)

    def move(self):
        if not self.path_clear:
            self.pub.publish(Twist(angular=Vector3(z=self.ang_vel), linear=Vector3(x=0)))

        else:
            self.pub.publish(Twist(angular=Vector3(z=0), linear=Vector3(x=self.lin_vel)))

    def run(self):
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            time.sleep(1)
            self.move()
            r.sleep()

if __name__ == '__main__':
    w = ObjectAvoider()
    w.run()



