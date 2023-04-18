#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion,quaternion_from_euler
from geometry_msgs.msg import Point , Twist, Quaternion
from math import atan2  ,pi
from std_msgs.msg import Float32 , Float64
import math

x = 0.0 
y = 0.0
theta = 0.0
rot_q_w = 0.0
rot_q_z = 0.0

class RobotMover:
    def __init__(self):




        rospy.init_node('robot_mover', anonymous=True)
        rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.pub_1 = rospy.Publisher("/inc_x", Float32, queue_size=1)
        self.pub_2 = rospy.Publisher("/inc_y", Float32, queue_size=1)
        self.pub_3 = rospy.Publisher("/angle_to_goal", Float64, queue_size=1)
        self.robot_pose = Point()
        self.robot_yaw = 0.0

    def odom_callback(self, odom_msg):
        # Save robot's current position and orientation
        self.robot_pose = odom_msg.pose.pose.position
        self.robot_yaw = 2*atan2(odom_msg.pose.pose.orientation.z, odom_msg.pose.pose.orientation.w)

    def newOdom (self, msg):
        global x , y, theta ,rot_q_z ,rot_q_w
        # global y
        # global theta 

        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y

        rot_q = msg.pose.pose.orientation
        rot_q_z = rot_q.z
        rot_q_w = rot_q.w
        (roll , pitch , theta) = euler_from_quaternion([rot_q.x , rot_q.y ,rot_q.z , rot_q.w])


    def move_towards_goal(self):
        twist = Twist()
        while True:
            # Compute distance and angle errors
            dist_error = ((goal_point.x - self.robot_pose.x)**2 + (goal_point.y - self.robot_pose.y)**2)**0.5
            angle_error = goal_orientation - self.robot_yaw

            # Adjust twist according to errors and error tolerances
            if abs(angle_error) > angle_tolerance:
                twist.linear.x = 0.0
                twist.angular.z = angular_speed if angle_error > 0.0 else -angular_speed
            elif abs(dist_error) > distance_tolerance:
                twist.linear.x = linear_speed
                twist.angular.z = 0.0
            else:
                twist.linear.x = 0.0
                twist.angular.z = 0.0
                self.cmd_vel_pub.publish(twist)
                break

            # Publish twist and sleep
            self.cmd_vel_pub.publish(twist)
            rospy.sleep(0.1)

if __name__ == '__main__':
    robot_mover = RobotMover()
    robot_mover.move_towards_goal()