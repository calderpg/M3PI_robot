#!/usr/bin/python

from SwarmBot import *
from RadioLink import *
from DriveController import *
import time

import roslib; roslib.load_manifest('M3Pi')
import rospy

from geometry_msgs.msg import Twist


class M3PiBotDriver:
    def __init__(self, port):
        rospy.init_node('M3Pi_Driver')
        self.radio_link = BASE_COMM_LINK(port, 9600)
        self.robot = SWARMBOT("ROS", self.radio_link)
        self.controller = TankDrive()
        self.m0 = 0.0
        self.m1 = 0.0
        rospy.Subscriber("cmd_vel", Twist, self.callback)
        rate = rospy.Rate(rospy.get_param('~hz', 32))
        self.last_time = time.clock()
        while not rospy.is_shutdown():
            rate.sleep()
            new_time = time.clock()
            time_difference = new_time - self.last_time
            if time_difference >= 1.0:
                self.m0 = 0.0
                self.m1 = 0.0
            self.robot.Tank_Drive(self.m0, self.m1)

    def callback(self, data):
        """Send Twist commands to the robot"""
        X = data.linear.x
        Z = data.angular.z
        commands = self.controller.Compute(X, Z)
        self.last_time = time.clock()
        self.m0 = commands[1]
        self.m1 = commands[0]


if __name__ == "__main__":
    port = "/dev/ttyUSB0"
    #port = rospy.get_param("VexBot_Driver/port")
    M3PiBotDriver(port)
