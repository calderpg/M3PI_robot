#!/usr/bin/env python

import sys
import roslib; roslib.load_manifest('M3Pi')
import rospy

from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from std_msgs.msg import String


class Teleop:
    def __init__(self):
        rospy.init_node('M3PiBot_Teleop')

        self.x_axis = 1 #number of up-down axis on left analog stick
        self.y_axis = 0 #number of left-right axis on left analog stick
        self.deadman_button = 0 #number of green button
        self.last_analog_X = 0.0
        self.last_analog_Y = 0.0
        self.cmd_pub = rospy.Publisher('cmd_vel', Twist)

        rospy.Subscriber("joy", Joy, self.NewState)
        rate = rospy.Rate(rospy.get_param('~hz', 60))
        
        while not rospy.is_shutdown():
            rate.sleep()
            cleaned = self.Convert(self.last_analog_X, self.last_analog_Y)
            self.Publish(cleaned)
                

    def Convert(self, X, Y):
        """ Converts raw joystick axis values into linear and angular movement commands """
        #Control variables (empirically determined) [these should be the same as found in the driver node]
        max_linear = 1.0
        min_linear = 0.1
        max_angular = 1.0
        min_angular = 0.1
        #Convert values to known range
        X_mapped = self.Map(X, min_linear, max_linear)
        Z_mapped = self.Map(Y, min_angular, max_angular)
        #Return values
        return [X_mapped, Z_mapped]

    def Map(self, value, min_value, max_value):
        """Takes a value between -1.0 and 1.0 and maps it appropriately to the ranges (-max to -min) or (min to max)"""
        if value == 0.0 or value == -0.0:
            return 0.0
        else:
            sign = 1.0
            if value < 0.0:
                sign = -1.0
            value_range = max_value - min_value
            magnitude = min_value + (value_range * abs(value))
            #Return value
            return (magnitude * sign)

    def Publish(self, cleaned):
        """Take normalized data, make Twist message. """
        cmd = Twist()
        cmd.linear.x = cleaned[0]
        cmd.angular.z = cleaned[1]
        self.cmd_pub.publish(cmd)

    def NewState(self, data):
        """Receive joystick data, save it in the state storage variables"""
        if data.buttons[self.deadman_button] == 1:
            self.last_analog_X = data.axes[self.x_axis]
            self.last_analog_Y = data.axes[self.y_axis]
        else:
            self.last_analog_X = 0.0
            self.last_analog_Y = 0.0


if __name__ == "__main__":
    Teleop()
