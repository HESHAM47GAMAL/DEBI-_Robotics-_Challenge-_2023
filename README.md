# DEBI-_Robotics-_Challenge-_2023🔥🔥🔥🤖🤖🤖
- [Description](#Description)
- [Steps](#Steps)
  - [Arm](#Arm)
  - [Turtle](#Turtle)
  - [Link Arm with Turtle](#Link-Arm-with-Turtle)
  - [Enviroment](#Enviroment)   
  


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
 
  
  <p> for more info follow <a href="https://emanual.robotis.com/docs/en/platform/openmanipulator_x/ros_simulation/#launch-gazebo" >🔗Press</a> </p>

### Turtle


### Link Arm with Turtle

### Enviroment
