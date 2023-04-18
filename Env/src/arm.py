#!/usr/bin/env python3
import rospy
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

def main():
    rospy.init_node('open_manipulator_controller')

    # Create an action client for the '/arm_controller/follow_joint_trajectory' action
    client = actionlib.SimpleActionClient('/arm_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
    client.wait_for_server()

    # Define the joint names and the target joint positions
    joint_names = ['joint1', 'joint2', 'joint3', 'joint4']
    target_positions = [0,0.650,0.100,0.00]

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

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass