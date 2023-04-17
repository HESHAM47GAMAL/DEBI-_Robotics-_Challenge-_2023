#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point , Twist
from math import atan2
from std_msgs.msg import Float32

x = 0.0 
y = 0.0
theta = 0.0

def newOdom (msg):
    global x
    global y
    global theta 

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    rot_q = msg.pose.pose.orientation
    (roll , pitch , theta) = euler_from_quaternion([rot_q.x , rot_q.y ,rot_q.z , rot_q.w])

rospy.init_node("control_Robot")

sub = rospy.Subscriber("/odom", Odometry, newOdom)
pub = rospy.Publisher("/cmd_vel", Twist , queue_size=1 )
pub_1 = rospy.Publisher("/inc_x", Float32, queue_size=1)
pub_2 = rospy.Publisher("/inc_y", Float32, queue_size=1)
pub_3 = rospy.Publisher("/angle_to_goal", Float32, queue_size=1)

speed = Twist()

r = rospy.Rate(20)

goal = Point()
goal.x = -0.79917
goal.y = 0.25512


while not rospy.is_shutdown():
    inc_x = goal.x - x
    inc_y = goal.y -y

    angle_to_goal = atan2(inc_y , inc_x)

    if abs(angle_to_goal - theta) > 0.1:
        speed.linear.x = 0.0
        speed.angular.z = 0.1

    else :
        speed.linear.x = 0.1
        speed.angular.z = 0.0

    if( ( inc_x < 0.00001 ) and ( inc_y < 0.00001 ) ):
        speed.linear.x = 0.0
        speed.angular.z = 0.0
        rospy.loginfo("Target Catch!")
    
    pub.publish(speed)
    pub_1.publish(inc_x)
    pub_2.publish(inc_y)
    pub_3.publish(angle_to_goal)
    r.sleep()




