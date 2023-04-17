#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

class TurtleBot3:
    def __init__(self):
        rospy.init_node('turtlebot3_controller')
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.odom = Odometry()

    def odom_callback(self, msg):
        self.odom = msg

    def move_to_position(self, x_goal, y_goal, distance_tolerance=0.01):
        rate = rospy.Rate(10)
        cmd_vel = Twist()
        while not rospy.is_shutdown():
            x_current = self.odom.pose.pose.position.x
            y_current = self.odom.pose.pose.position.y
            distance = ((x_goal - x_current) ** 2 + (y_goal - y_current) ** 2) ** 0.5

            if distance < distance_tolerance:
                break

            cmd_vel.linear.x = 0.2 
            cmd_vel.angular.z = 4 * (y_goal - y_current) / distance
            self.cmd_vel_pub.publish(cmd_vel)

            rate.sleep()

if __name__ == '__main__':
    try:
        bot = TurtleBot3()
        bot.move_to_position(-0.1, 0.422963)
    except rospy.ROSInterruptException:
        pass