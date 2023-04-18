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

goal = Point()
goal.x = -0.8010
goal.y = 0.2359
goal.z = 0.7316
# Set the orientation of the goal point
# (roll, pitch, yaw) = (0.0, 0.0, pi/2)  # set the orientation to 90 degrees (pi/2 radians)
# q = quaternion_from_euler(roll, pitch, yaw)
# goal_orientation = Quaternion(*q)
# goal.orientation = goal_orientation

goal_reached = False
X_reached  = True 
X_back  = 1
orientation_reached = 0 
y_reached = 0




while not rospy.is_shutdown():
    while(not goal_reached):
        inc_x = goal.x - x
        inc_y = goal.y -y

        rospy.loginfo("check is %s", (abs(inc_x) > 0.005) and  X_reached)

        ## to catch X position 
        if (abs(inc_x) > 0.005)    :
            
            if(inc_x) > 0.001 :
                X_back = 0
                #edit oreintation of robot first
                condition = True
                while ( condition):
                    rospy.loginfo("try to catch X in front")
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
                
                #move to target X
                while(inc_x > 0.001):
                    rospy.loginfo("try to catch X and move X +")
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

            # elif(inc_x) < -0.001  :
            # #edit oreintation of robot first
            #     X_front = 0
            #     condition = True
            #     while ( condition):
            #         rospy.loginfo("try to catch X in back")
            #         if(rot_q_w > 0 ):
            #             speed.angular.z = 0.05
            #             if(rot_q_w < 0.001):
            #                 condition = False
            #                 speed.angular.z = 0.0

            #         else :
            #             speed.angular.z = 0.05
            #             if(rot_q_z > -0.001):
            #                 condition = False
            #                 speed.angular.z = 0.0

            #         speed.linear.x = 0.0
            #         inc_x = goal.x - x
            #         pub_1.publish(inc_x)
            #         pub.publish(speed)
            #     #move to target X
            #     while(inc_x < -0.001):
            #         rospy.loginfo("try to catch X and move X -")
            #         #update reading 
            #         inc_x = goal.x - x
            #         inc_y = goal.y -y
            #         speed.linear.x = 0.1 
            #         #if ((inc_x > 0.001) or (inc_y > 0.001) ) else -0.1
            #         speed.angular.z = 0.0
            #         #publish data to monitor
            #         pub.publish(speed)
            #         pub_1.publish(inc_x)
            #         pub_2.publish(inc_y)
            #     rospy.loginfo("finished X - ")
            #     speed.linear.x = 0.0
            #     speed.angular.z = 0.0
            #     pub.publish(speed)

   

        # Adjust the linear and angular velocities based on the angle difference
        # abs(angle_diff) > 0.1 or
        elif abs(rot_q_z - goal.z) > 0.001 : 
            rospy.loginfo("Catch orientation")
            # if(rot_q_z - goal.z)
            speed.linear.x = 0.0
            speed.angular.z = 0.1 if rot_q_z < goal.z else -0.05


            

        elif y_reached == 1 :
            speed.linear.x = 0.1 
            #if ((inc_x > 0.001) or (inc_y > 0.001) ) else -0.1
            speed.angular.z = 0.0
        if  inc_y < 0.006 and abs(rot_q_z - goal.z) < 0.001:
                speed.linear.x = 0.0
                speed.angular.z = 0.0
                rospy.loginfo("Target Reached!")
                goal_reached = True
        # #and abs(angle_diff)
        # if inc_x < 0.05  or inc_y < 0.06 :
        #     rospy.loginfo("One catched !")
        #     if(inc_x > 0.005):
        #         while (round(rot_q_z, 1) != 0):
        #             rospy.loginfo("try to catch X")
        #             if(rot_q_z > 0 ):
        #                 speed.angular.z = -0.05
        #             else :
        #                 speed.angular.z = 0.05
        #             speed.linear.x = 0.0
        #             pub.publish(speed)
        #     speed.linear.x = 0.0
        #     if inc_x < 0.005  and inc_y < 0.006 and abs(rot_q_z - goal.z) < 0.001:
        #         speed.linear.x = 0.0
        #         speed.angular.z = 0.0
        #         rospy.loginfo("Target Reached!")
        #         goal_reached = True




            

        # 👀️ old code
        # if abs(angle_to_goal - theta) > 0.1:
        #     speed.linear.x = 0.0
        #     speed.angular.z = 0.1

        # else :
        #     speed.linear.x = 0.1
        #     speed.angular.z = 0.0

        # if( ( inc_x < 0.00001 ) and ( inc_y < 0.00001 ) ):
        #     speed.linear.x = 0.0
        #     speed.angular.z = 0.0
        #     rospy.loginfo("Target Catch!")
        #     goal_reached = True
        
        pub.publish(speed)
        pub_1.publish(inc_x)
        pub_2.publish(inc_y)
        pub_3.publish(rot_q_z - goal.z)
        r.sleep()
    while(goal_reached):
        rospy.loginfo("Target Catch! ,wait New")






# #!/usr/bin/env python3
# import rospy
# from nav_msgs.msg import Odometry
# from tf.transformations import euler_from_quaternion
# from geometry_msgs.msg import Point , Twist
# from math import atan2
# from std_msgs.msg import Float32

# x = 0.0 
# y = 0.0
# theta = 0.0

# def newOdom (msg):
#     global x
#     global y
#     global theta 

#     x = msg.pose.pose.position.x
#     y = msg.pose.pose.position.y

#     rot_q = msg.pose.pose.orientation
#     (roll , pitch , theta) = euler_from_quaternion([rot_q.x , rot_q.y ,rot_q.z , rot_q.w])

# rospy.init_node("control_Robot")

# sub = rospy.Subscriber("/odom", Odometry, newOdom)
# pub = rospy.Publisher("/cmd_vel", Twist , queue_size=1 )
# pub_1 = rospy.Publisher("/inc_x", Float32, queue_size=1)
# pub_2 = rospy.Publisher("/inc_y", Float32, queue_size=1)
# pub_3 = rospy.Publisher("/angle_to_goal", Float32, queue_size=1)

# speed = Twist()

# r = rospy.Rate(20)

# goal = Point()
# goal.x = -0.79917
# goal.y = 0.25512


# while not rospy.is_shutdown():
#     inc_x = goal.x - x
#     inc_y = goal.y -y

#     angle_to_goal = atan2(inc_y , inc_x)

#     if abs(angle_to_goal - theta) > 0.1:
#         speed.linear.x = 0.0
#         speed.angular.z = 0.1

#     else :
#         speed.linear.x = 0.1
#         speed.angular.z = 0.0

#     if( ( inc_x < 0.00001 ) and ( inc_y < 0.00001 ) ):
#         speed.linear.x = 0.0
#         speed.angular.z = 0.0
#         rospy.loginfo("Target Catch!")
    
#     pub.publish(speed)
#     pub_1.publish(inc_x)
#     pub_2.publish(inc_y)
#     pub_3.publish(angle_to_goal)
#     r.sleep()
