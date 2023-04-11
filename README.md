# DEBI-_Robotics-_Challenge-_2023🔥🔥🔥🤖🤖🤖
- [Description](#Description)
- [Steps](#Steps)
  - [Arm](#Arm)
  - [Turtle](#Turtle)
- [🔥Turtle openManipulator](#Turtle-openManipulator)
- [Enviroment](#Enviroment)   
  - [Create World](#Create-world)
  - [Launch Robot with map](#Launch-Robot-with-map)
- [Get Start🏃‍♂️️](#Get-start)
  


## Description
<p> ⚡️ it's competition for robotics to search for bools in own half of track an catch it using arm and throw it in half contender 


## Steps
  <p> ⚡️Here I will describe steps to make robot work and do it 

### Arm 
<p> ⚡️ follow setup
<p> 1.Install dependent pacakges (🙆‍♂️️version Noetic )
  
```console
  sudo apt-get install ros-noetic-ros-controllers ros-noetic-gazebo* ros-noetic-moveit* ros-noetic-industrial-core
  sudo apt install ros-noetic-dynamixel-sdk ros-noetic-dynamixel-workbench*
  sudo apt install ros-noetic-robotis-manipulator
```
<p> 2.Download and build OpenMANIPULATOR-X packages (but 👀️👀️👀️ I clone those and pressent in this repo)
  
  ```console
  git clone -b noetic-devel https://github.com/ROBOTIS-GIT/open_manipulator.git
  git clone -b noetic-devel https://github.com/ROBOTIS-GIT/open_manipulator_msgs.git
  git clone -b noetic-devel https://github.com/ROBOTIS-GIT/open_manipulator_simulations.git
  git clone https://github.com/ROBOTIS-GIT/open_manipulator_dependencies.git
```
  
 <p> To start moving Arm in Gazebo follow steps 
   
 ```console
  roslaunch open_manipulator_gazebo open_manipulator_gazebo.launch
  ```
  
  <p> 👀️👀️👀️👀️👀️👀️👀️👀️👀️👀️👀️👀️ Don't forget press on fucken pitch play button 🙃
    
  ```console
  roslaunch open_manipulator_controller open_manipulator_controller.launch use_platform:=false
  roslaunch open_manipulator_control_gui open_manipulator_control_gui.launch 
  ```
  
  <p>
    ⚡️node & topics connection graph
  <img src = "https://github.com/HESHAM47GAMAL/DEBI-_Robotics-_Challenge-_2023/blob/main/pic_github/Gazebo.png"/>
  </p>
 
  
  <p> for more info follow <a href="https://emanual.robotis.com/docs/en/platform/openmanipulator_x/ros_simulation/#launch-gazebo" >🔗Press</a> </p>

### Turtle
<p> ⚡️ follow setup
<p> 1.Install Dependent ROS Packages (🙆‍♂️️version Noetic )

```console
sudo apt-get install ros-noetic-joy ros-noetic-teleop-twist-joy \
  ros-noetic-teleop-twist-keyboard ros-noetic-laser-proc \
  ros-noetic-rgbd-launch ros-noetic-rosserial-arduino \
  ros-noetic-rosserial-python ros-noetic-rosserial-client \
  ros-noetic-rosserial-msgs ros-noetic-amcl ros-noetic-map-server \
  ros-noetic-move-base ros-noetic-urdf ros-noetic-xacro \
  ros-noetic-compressed-image-transport ros-noetic-rqt* ros-noetic-rviz \
  ros-noetic-gmapping ros-noetic-navigation ros-noetic-interactive-markers
  ```
  <p> 2.Install TurtleBot3 Packages
  
  ```console
  sudo apt install ros-noetic-dynamixel-sdk
  sudo apt install ros-noetic-turtlebot3-msgs
  sudo apt install ros-noetic-turtlebot3
  ```

# 🔥Turtle openManipulator
<p> Download and build packages
  
```console
  git clone https://github.com/ROBOTIS-GIT/turtlebot3_manipulation.git
  git clone https://github.com/ROBOTIS-GIT/turtlebot3_manipulation_simulations.git
  git clone https://github.com/ROBOTIS-GIT/open_manipulator_dependencies.git
```

<p> May face problem in build due to moveitmsgs & object_recognition_msgs,octomap-msgs ,moveit core , plane interface to solve them 
  
```console 
  git clone https://github.com/ros-planning/moveit_msgs.git
  sudo apt-get install ros-noetic-object-recognition-msgs
  sudo apt-get install ros-noetic-octomap-msgs
  sudo apt-get install ros-noetic-moveit-core
  sudo apt-get install ros-noetic-moveit-ros-planning
  sudo apt-get install ros-noetic-moveit-ros-planning-interface
  ```
<p> 🙀️ save time of select robot type and run in terminal 
  
```console 
  echo 'export TURTLEBOT3_MODEL=waffle_pi' >> ~/.bashrc
```
  
<p> ⚡️ To launch Robot in Gazebo 
  
```console
  roslaunch turtlebot3_manipulation_gazebo turtlebot3_manipulation_gazebo.launch
```
  
<p>  press [▶] button in Gazebo to start simulation
<p> ⚡️ To 🎮️control arm and moving of Robot 
  
```console
  roslaunch turtlebot3_manipulation_moveit_config move_group.launch
  roslaunch turtlebot3_manipulation_gui turtlebot3_manipulation_gui.launch
  roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch
```
  
# Enviroment
<p>🤯️ it's really easy to create your own Emviroment and launch it with Robot follow with me 🤩️
  
## Create World  
<p> To do this you can Follow this link and give you basics to create it <a href="https://www.youtube.com/watch?v=S8pwfsK-F9w&ab_channel=KienTran" >🔗Press</a>
  
##  Launch Robot with map
<p> It's easy 🤷‍♂️️😎️ follow with me 
<p> go to launch file that use for launch robot and write in Arguement section 
  
 ```console
  <arg name="world_file" default="$(find Env)/worlds/Track.world"/>
```
<p> and after Arguements write 

```console 
   <!-- Gazebo empty world launch file -->
    <include file="$(find gazebo_ros)/launch/empty_world.launch">
        <arg name="world_name" value="$(arg world_file)"/>
        <arg name="paused"  value="$(arg paused)"/>
        <arg name="use_sim_time" value="$(arg use_sim_time )"/>
        <arg name="gui" value="$(arg gui)"/>
        <arg name="recording" value="$(arg recording)"/>
        <arg name="debug" value="$(arg debug)"/>
        
    </include>
```
<p> take look on Env folder in Repo   
  
<p >
  <img src="https://github.com/HESHAM47GAMAL/DEBI-_Robotics-_Challenge-_2023/blob/main/pic_github/Track.png"
  </p>

  
# Get Start🏃‍  
<p> What are you Wait!!!!!!  get clone and try 
<p> To launch Robot and control
  
```console
 roslaunch Env Track.launch
 roslaunch turtlebot3_manipulation_moveit_config move_group.launch 
 roslaunch turtlebot3_manipulation_gui turtlebot3_manipulation_gui.launch
 roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch
```
