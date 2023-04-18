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
def newOdom (msg):
    global x , y, theta ,rot_q_z ,rot_q_w
    # global y
    # global theta 

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    rot_q = msg.pose.pose.orientation
    rot_q_z = rot_q.z
    rot_q_w = rot_q.w
    (roll , pitch , theta) = euler_from_quaternion([rot_q.x , rot_q.y ,rot_q.z , rot_q.w])

rospy.init_node("control_Robot")
sub = rospy.Subscriber("/odom", Odometry, newOdom)
pub = rospy.Publisher("/cmd_vel", Twist , queue_size=1 )
pub_1 = rospy.Publisher("/inc_x", Float32, queue_size=1)
pub_2 = rospy.Publisher("/inc_y", Float32, queue_size=1)
pub_3 = rospy.Publisher("/angle_to_goal", Float64, queue_size=1)

speed = Twist()
r = rospy.Rate(50)
points = []
goal = Point()
goal.x = -0.8010
goal.y = 0.2359
goal.z = 0.0
points.append(goal)
goal_reached = False

while not rospy.is_shutdown():
    while(not goal_reached):
        inc_x = goal.x - x
        inc_y = goal.y -y
        if abs(rot_q_z - goal.z) > 0.001 : 
            rospy.loginfo("Catch orientation")
            # if(rot_q_z - goal.z)
            speed.linear.x = 0.0
            speed.angular.z = 0.1 if rot_q_z < goal.z else -0.05


            

        else :
            rospy.loginfo("Catch position")
            speed.linear.x = 0.1 
            #if ((inc_x > 0.001) or (inc_y > 0.001) ) else -0.1
            speed.angular.z = 0.0
        if  inc_y < 0.006 and abs(rot_q_z - goal.z) < 0.001:
                speed.linear.x = 0.0
                speed.angular.z = 0.0
                rospy.loginfo("Target Reached!")
                goal_reached = True
