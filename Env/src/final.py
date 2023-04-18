#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion,quaternion_from_euler
from geometry_msgs.msg import Point , Twist, Quaternion
from math import atan2  ,pi
from std_msgs.msg import Float32 , Float64
import math
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

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
    rospy.loginfo("get new data")

sub = rospy.Subscriber("/odom", Odometry, newOdom)
pub = rospy.Publisher("/cmd_vel", Twist , queue_size=1 )
pub_1 = rospy.Publisher("/inc_x", Float32, queue_size=1)
pub_2 = rospy.Publisher("/inc_y", Float32, queue_size=1)
pub_3 = rospy.Publisher("/angle_to_goal", Float64, queue_size=1)

##for Arm 



rospy.init_node("control_Robot")



speed = Twist()

r = rospy.Rate(50)

goal = Point()


def get_x_pos():
    condition = True
    while ( condition):
        #edit oreintation of robot first
        rospy.loginfo("try to catch X in front")
        rospy.loginfo("rot_q_z is %s", rot_q_z)
        if(rot_q_z > 0 ):  ### here may need to take abs of rot_q_z
            speed.angular.z = -0.05
            if(rot_q_z < 0.001):
                condition = False
                speed.angular.z = 0.0

        else :
            speed.angular.z = 0.05
            if(rot_q_z > -0.001):
                condition = False
                speed.angular.z = 0.0

        speed.linear.x = 0.0
        pub.publish(speed)
    inc_x = goal.x - x
    inc_y = goal.y -y
    rospy.loginfo("inc_x is %s", inc_x)
    #move to target X
    while(inc_x > 0.001):
        rospy.loginfo("try to catch X and move X +")
        rospy.loginfo("inc_x is %s", inc_x)
        #update reading 
        inc_x = goal.x - x
        inc_y = goal.y -y

        speed.linear.x = 0.1 
        #if ((inc_x > 0.001) or (inc_y > 0.001) ) else -0.1
        speed.angular.z = 0.0
        #publish data to monitor
        pub.publish(speed)
        pub_1.publish(inc_x)
        pub_2.publish(inc_y)
    rospy.loginfo("finished X +")
    speed.linear.x = 0.0
    speed.angular.z = 0.0
    pub.publish(speed)

def get_x_neg():
    condition = True
    while ( condition):
        rospy.loginfo("try to catch X in back")
        if(rot_q_w > 0 ):
            speed.angular.z = 0.05
            if(rot_q_w < 0.001):
                condition = False
                speed.angular.z = 0.0

        else :
            speed.angular.z = 0.05
            if(rot_q_z > -0.001):
                condition = False
                speed.angular.z = 0.0

        speed.linear.x = 0.0
        inc_x = goal.x - x
        pub_1.publish(inc_x)
        pub.publish(speed)
    #move to target X
    while(inc_x < -0.001):
        rospy.loginfo("try to catch X and move X -")
        #update reading 
        inc_x = goal.x - x
        inc_y = goal.y -y
        speed.linear.x = 0.1 
        #if ((inc_x > 0.001) or (inc_y > 0.001) ) else -0.1
        speed.angular.z = 0.0
        #publish data to monitor
        pub.publish(speed)
        pub_1.publish(inc_x)
        pub_2.publish(inc_y)
    rospy.loginfo("finished X - ")
    speed.linear.x = 0.0
    speed.angular.z = 0.0
    pub.publish(speed)

def rotate():
    # rospy.loginfo("angle dif is %s", rot_q_z - goal.z)
    # rospy.loginfo("angle  is %s", rot_q_z )
    rospy.loginfo("Catch orientation")
    while(rot_q_z - goal.z < 0.001):
        rospy.loginfo("angle is %s", rot_q_z - goal.z)
        # if(rot_q_z - goal.z)
        speed.linear.x = 0.0
        speed.angular.z = 0.08 if rot_q_z < goal.z else -0.08
        pub.publish(speed)
    speed.angular.z = 0.0
    speed.linear.x = 0.0
    pub.publish(speed)
    rospy.loginfo("finished Rotation")


def get_y_pos():
    inc_x = goal.x - x
    inc_y = goal.y -y
    rospy.loginfo("inc_y is %s", inc_y)
    # move to target y
    while(inc_y > 0.001):
        rospy.loginfo("try to catch Y and move Y +")
        rospy.loginfo("inc_y is %s", inc_y)
        #update reading 
        inc_x = goal.x - x
        inc_y = goal.y -y

        speed.linear.x = 0.1 
        #if ((inc_x > 0.001) or (inc_y > 0.001) ) else -0.1
        speed.angular.z = 0.0
        #publish data to monitor
        pub.publish(speed)
        pub_1.publish(inc_x)
        pub_2.publish(inc_y)
    rospy.loginfo("finished Y +")
    speed.linear.x = 0.0
    speed.angular.z = 0.0
    pub.publish(speed)

def get_arm(x,y,z,w):
    
       # Create an action client for the '/arm_controller/follow_joint_trajectory' action
    client = actionlib.SimpleActionClient('/arm_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
    client.wait_for_server()

    # Define the joint names and the target joint positions
    joint_names = ['joint1', 'joint2', 'joint3', 'joint4']
    target_positions = [x,y,z,w]

    # Create a joint trajectory message
    trajectory = JointTrajectory()
    trajectory.joint_names = joint_names

    # Create a trajectory point with the target positions and a duration to reach the target
    point = JointTrajectoryPoint()
    point.positions = target_positions
    point.time_from_start = rospy.Duration(2.0)

    # Add the trajectory point to the joint trajectory
    trajectory.points = [point]

    # Create and send the goal to the action server
    goal = FollowJointTrajectoryGoal()
    goal.trajectory = trajectory
    client.send_goal(goal)

    # Wait for the result
    client.wait_for_result()

    rospy.loginfo("Arm moved ")

def get_grip(position, duration):
    client = actionlib.SimpleActionClient('/gripper_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
    client.wait_for_server()

    # Define the joint names
    joint_names = ['gripper']

    # Create the joint trajectory message
    trajectory = JointTrajectory()
    trajectory.joint_names = joint_names

    # Create the joint trajectory point
    point = JointTrajectoryPoint()
    point.positions = [position]
    point.time_from_start = rospy.Duration(duration)

    trajectory.points = [point]

    # Create the goal message
    goal = FollowJointTrajectoryGoal()
    goal.trajectory = trajectory

    # Send the goal to the action server
    client.send_goal(goal)
    client.wait_for_result(rospy.Duration.from_sec(5.0))
    rospy.loginfo("Gripper  ")




if __name__ == '__main__':
    
    rospy.loginfo("I am in main ")
    rospy.loginfo("I am in main ")
    rospy.loginfo("I am in main ")
    goal.x = -0.7510
    goal.y = 0.235
    goal.z = 0.7316
    get_arm(0,0.850,0.100,0.00)
    get_grip(position= 0.012, duration=1.0) # Open the gripper
    get_x_pos()
    rotate()
    get_y_pos()
    get_grip(position= -0.014, duration=1.0) # Open the gripper