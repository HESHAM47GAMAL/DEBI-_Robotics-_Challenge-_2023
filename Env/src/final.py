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
    # rospy.loginfo("get new data")

sub = rospy.Subscriber("/odom", Odometry, newOdom)
pub = rospy.Publisher("/cmd_vel", Twist , queue_size=1 )
pub_1 = rospy.Publisher("/inc_x", Float32, queue_size=1)
pub_2 = rospy.Publisher("/inc_y", Float32, queue_size=1)
pub_3 = rospy.Publisher("/angle_to_goal", Float64, queue_size=1)

##for Arm 



rospy.init_node("control_Robot")



speed = Twist()

r = rospy.Rate(30)

goal = Point()


def get_x_pos(linear =0.1 , angle =0.05): ##0.1 , 0.05
    condition = True
    while ( condition):
        #edit oreintation of robot first
        # rospy.loginfo("try to catch X in front")
        # rospy.loginfo("rot_q_z is %s", rot_q_z)
        if(rot_q_z > 0 ):  ### here may need to take abs of rot_q_z
            speed.angular.z = -angle##-0.05
            if(rot_q_z < 0.001):
                condition = False
                speed.angular.z = 0.0

        else :
            speed.angular.z = angle##0.05
            if(rot_q_z > -0.001):
                condition = False
                speed.angular.z = 0.0

        speed.linear.x = 0.0
        pub.publish(speed)
    inc_x = goal.x - x
    inc_y = goal.y -y
    # rospy.loginfo("inc_x is %s", inc_x)
    #move to target X
    while(inc_x > 0.001):
        # rospy.loginfo("try to catch X and move X +")
        # rospy.loginfo("inc_x is %s", inc_x)
        #update reading 
        inc_x = goal.x - x
        inc_y = goal.y -y

        speed.linear.x = linear
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
        # rospy.loginfo("try to catch X in back")
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
        # rospy.loginfo("try to catch X and move X -")
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

def rotate_pos(angle):
    # rospy.loginfo("angle dif is %s", rot_q_z - goal.z)
    # rospy.loginfo("angle  is %s", rot_q_z )
    # rospy.loginfo("Catch orientation + ")
    while(rot_q_z - goal.z < 0.001):
        # rospy.loginfo("angle is %s", rot_q_z - goal.z)
        # if(rot_q_z - goal.z)
        speed.linear.x = 0.0
        speed.angular.z = angle if rot_q_z < goal.z else -angle ##0.08
        pub.publish(speed)
    speed.angular.z = 0.0
    speed.linear.x = 0.0
    pub.publish(speed)
    rospy.loginfo("finished Rotation")

def rotate_neg(angle):
    # rospy.loginfo("angle dif is %s", rot_q_z - goal.z)
    # rospy.loginfo("angle  is %s", rot_q_z )
    # rospy.loginfo("Catch orientation  - ")
    while(rot_q_z - goal.z > 0.001):
        # rospy.loginfo("angle is %s", rot_q_z - goal.z)
        # if(rot_q_z - goal.z)
        speed.linear.x = 0.0
        speed.angular.z = angle 
        ##if rot_q_z < goal.z else -angle ##0.08
        pub.publish(speed)
    speed.angular.z = 0.0
    speed.linear.x = 0.0
    pub.publish(speed)
    rospy.loginfo("finished Rotation")



def get_y_pos():
    inc_x = goal.x - x
    inc_y = goal.y -y
    # rospy.loginfo("inc_y is %s", inc_y)
    # move to target y
    while(inc_y > 0.001):
        # rospy.loginfo("try to catch Y and move Y +")
        # rospy.loginfo("inc_y is %s", inc_y)
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

def get_y_neg():
    inc_y = goal.y -y
    # rospy.loginfo("inc_y is %s", inc_y)
    while(inc_y < 0.001):
        # rospy.loginfo("try to catch Y and move Y +")
        # rospy.loginfo("inc_y is %s", inc_y)
        #update reading 
        inc_y = goal.y -y

        speed.linear.x = 0.1 
        #if ((inc_x > 0.001) or (inc_y > 0.001) ) else -0.1
        speed.angular.z = 0.0
        #publish data to monitor
        pub.publish(speed)
        pub_2.publish(inc_y)
    rospy.loginfo("finished Y -")
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

def back():
    inc_x = goal.x - x
    # rospy.loginfo("Back")
    # rospy.loginfo("inc_x is %s", inc_x)
    #move to target X
    while(inc_x < 0.001):
        # rospy.loginfo("try to catch X in back")
        # rospy.loginfo("inc_x is %s", inc_x)
        #update reading 
        inc_x = goal.x - x

        speed.linear.x = -0.1
        #if ((inc_x > 0.001) or (inc_y > 0.001) ) else -0.1
        speed.angular.z = 0.0
        #publish data to monitor
        pub.publish(speed)
        pub_1.publish(inc_x)
    rospy.loginfo("finished X back")
    speed.linear.x = 0.0
    speed.angular.z = 0.0
    pub.publish(speed)





if __name__ == '__main__':
    
    rospy.loginfo("control_Robot Created and here to serve ")

    ## 👀️👀️👀️👀️First goal to catch Green ball 
    goal.x = -1.0391    
    goal.y = 0.5021 ##0.5011
    goal.z = 0.712 ##0.711
    get_arm(0,0.860,0.100,0.050)
    get_grip(position= 0.022, duration=1.0) # Open the gripper
    get_x_pos(0.1,0.05)
    rospy.sleep(1)####
    rotate_pos(0.08)
    # rospy.sleep(1)###
    get_y_pos()
    rospy.sleep(1)
    goal.y = 0.5571
    rotate_pos(0.08)
    get_y_pos()
    # # rospy.sleep(3)
    get_grip(position= -0.018, duration=1.0)  #Close the gripper
    # # rospy.sleep(5)

    ## First goal to catch barrier to though ball 
    goal.x = -0.115
    goal.y = 0.5821
    goal.z = 0.9987
    get_arm(0,0.0,0.0,0.0)
    get_x_pos(0.2,0.15)
    get_arm(0,0.700, -0.700,0.00)   #angles to through ball in second half
    get_grip(position= 0.018, duration=1.0) # Open the gripper

    ## 👀️👀️👀️👀️Second goal to catch Green ball 
    goal.x = -0.3910
    goal.y = 0.1539
    goal.z = -0.7101 
    back()
    get_arm(0,0.860,0.100,0.050)
    rotate_neg(-0.08)
    get_y_neg()
    goal.y = 0.0915
    rospy.sleep(1)
    rotate_neg(-0.08)
    get_y_neg()
    get_grip(position= -0.018, duration=1.0)  #Close the gripper
    ## Second goal to catch barrier to though ball 
    goal.x = -0.115
    goal.y = 0.0971
    goal.z = -0.7101 
    get_arm(0,0.0,0.0,0.0)
    get_x_pos(0.2,0.15)
    get_arm(0,0.700, -0.700,0.00)   #angles to through ball in second half
    get_grip(position= 0.018, duration=1.0) # Open the gripper


    ## 👀️👀️👀️👀️third goal to catch Green ball 
    goal.x = -1.4715
    goal.y = -0.5001
    goal.z = -0.6754 #6744
    back()
    get_arm(0,0.860,0.100,0.050)
    get_grip(position= 0.018, duration=1.0) # Open the gripper
    rotate_neg(-0.08)
    goal.y = -0.5761
    goal.z = -0.6799
    rospy.sleep(1)
    rotate_neg(-0.08)
    get_y_neg()
    get_grip(position= -0.018, duration=1.0)  #Close the gripper
    ## Third goal to catch barrier to though ball 
    goal.x = -0.115
    goal.y = -0.5011
    # goal.z = -0.7101 
    get_arm(0,0.0,0.0,0.0)
    get_x_pos(0.2,0.15)
    get_arm(0,0.700, -0.700,0.00)   #angles to through ball in second half
    get_grip(position= 0.018, duration=1.0) # Open the gripper

    rospy.loginfo("Finally Three Balls Catched ")