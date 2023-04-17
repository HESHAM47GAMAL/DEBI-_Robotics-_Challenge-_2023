#!/usr/bin/env python3

import rospy
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

def send_gripper_command(position, duration):
    """
    Send a gripper command to the specified position with a duration.
    :param position: float, Position of the gripper
    :param duration: float, Duration of the movement
    """
    client = actionlib.SimpleActionClient('/gripper_control/follow_joint_trajectory', FollowJointTrajectoryAction)
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

if __name__ == '__main__':
    rospy.init_node('gripper_control_node')

    # Example: open and close the gripper
    send_gripper_command(position=1.0, duration=1.0)  # Open the gripper
    rospy.sleep(2.0)
    send_gripper_command(position=0.0, duration=1.0)  # Close the gripper
