#!/usr/bin/python

from SwarmBot import *
from RadioLink import *
from DriveController import *
import time

import roslib; roslib.load_manifest('M3Pi')
import rospy

from geometry_msgs.msg import Twist


class TWIST_TEST():
    def __init__(self):
        rospy.init_node('Tester')
        self.test_pub = rospy.Publisher("cmd_vel", Twist)
        rate = rospy.Rate(rospy.get_param('~hz', 32))
        while not rospy.is_shutdown():
            rate.sleep()
            message = Twist()
            message.linear.x = 0.75
            self.test_pub.publish(message)


if __name__ == "__main__":
    TWIST_TEST()
