# 4-Wheeled Mobile Robot – ROS 2 Navigation & Sensor Fusion

This repository contains the complete implementation of a **4-wheeled differential drive mobile robot** simulated using **ROS 2 Jazzy**, **Gazebo**, **SLAM Toolbox**, **robot_localization**, and the **Nav2 Navigation Stack**, with autonomous goal execution and **EKF-based sensor fusion** for drift reduction.

The project demonstrates correct usage of ROS 2 navigation architecture, differential drive simulation, Extended Kalman Filter configuration, SLAM mapping, AMCL localization, and runtime validation using RViz2 and rqt tools.

---

The repository is organized into three primary ROS 2 packages:

```text
tortoisebot_description/
├── urdf/              # Robot model (links, joints, sensors)
├── launch/            # robot_state_publisher launch files
└── package.xml

tortoisebot_gazebo/
├── launch/            # Gazebo spawn launch files
├── worlds/            # Gazebo world files
└── package.xml

tortoisebot_nav/
├── config/            # EKF, AMCL, Nav2 parameter YAML files
├── maps/              # Saved maps
├── launch/            # SLAM, localization, navigation launch files
└── package.xml
```

---

## Key Features

* 4-wheeled differential drive robot model  
* Accurate inertial and collision properties  
* Gazebo physics simulation  
* Wheel odometry publishing  
* IMU simulation  
* Sensor fusion using **robot_localization (EKF)**  
* Filtered odometry output (`/odometry/filtered`)  
* 2D SLAM mapping  
* AMCL-based localization  
* Autonomous navigation using **Nav2**  
* Goal execution and visualization in RViz2  

**NOTE**: Raw wheel odometry accumulates integration error over time (*drift*).  
The **Extended Kalman Filter (EKF)** fuses wheel odometry and IMU data to generate a stable `/odometry/filtered` output, which significantly improves localization accuracy and navigation stability.

---

## Software Requirements

* **ROS 2 Jazzy**
* Gazebo (via `ros_gz_sim`)
* Nav2
* SLAM Toolbox
* robot_localization
* rqt tools

### Required Packages

```bash
sudo apt install \
  ros-jazzy-ros-gz-sim \
  ros-jazzy-robot-localization \
  ros-jazzy-slam-toolbox \
  ros-jazzy-nav2-bringup \
  ros-jazzy-nav2-map-server \
  ros-jazzy-nav2-amcl \
  ros-jazzy-robot-state-publisher \
  ros-jazzy-joint-state-publisher \
  ros-jazzy-rqt \
  ros-jazzy-rqt-plot
```

---

## Build Instructions

```bash
# Create workspace
mkdir -p ~/nav_ws/src
cd ~/nav_ws/src

# Clone repository
git clone https://github.com/bineeshajabi/4-wheeled-robot_Navigation.git

# Build workspace
cd ~/nav_ws
colcon build --symlink-install

# Source workspace
source install/setup.bash
```

---

## Running the Simulation

### 1. Launch Gazebo and Spawn the Robot

```bash
ros2 launch tortoisebot_gazebo spawn_robot.launch.py
```

This will:

* Launch Gazebo using `ros_gz_sim`
* Spawn the 4-wheeled mobile robot
* Start `robot_state_publisher`

---

### 2. Launch Sensor Fusion (EKF)

```bash
ros2 launch tortoisebot_nav ekf.launch.py
```

This will:

* Fuse `/odom` and `/imu/data`
* Publish `/odometry/filtered`
* Improve odometry consistency and reduce drift

---

### 3. Run SLAM (Mapping Mode)

```bash
ros2 launch tortoisebot_nav slam.launch.py
```

To save the generated map:

```bash
ros2 run nav2_map_server map_saver_cli -f my_map
```

---

### 4. Run Localization

```bash
ros2 launch tortoisebot_nav localization.launch.py
```

This will:

* Load the saved map
* Start AMCL
* Estimate robot pose in the `map` frame

---

### 5. Start Autonomous Navigation

```bash
ros2 launch tortoisebot_nav navigation.launch.py
```

This will:

* Start Nav2 planner and controller servers
* Enable global and local costmaps
* Allow goal setting in RViz2

---

## TF Tree

You can visualize the TF structure using:

```bash
ros2 run tf2_tools view_frames
```

Expected TF hierarchy:

```text
map
 └── odom
      └── base_link
           ├── laser
           ├── imu_link
           └── wheels
```

(Insert TF diagram screenshot here if needed.)

---

## Runtime Validation

Check filtered odometry:

```bash
ros2 topic echo /odometry/filtered
```

Check TF frames:

```bash
ros2 run tf2_tools view_frames
```

Check active navigation nodes:

```bash
ros2 lifecycle nodes
```

Monitor pose estimation in RViz2 and verify stable localization during motion.

---

## Expected Behavior

* Robot spawns correctly in Gazebo  
* Sensors publish valid `/scan`, `/imu/data`, and `/odom`  
* EKF outputs stable `/odometry/filtered`  
* SLAM builds an accurate occupancy grid map  
* AMCL localizes robot reliably  
* Nav2 plans and executes autonomous paths  
* Robot reaches target goals without excessive drift  

---

## Conclusion

This project demonstrates a complete **ROS 2 mobile robot navigation system with sensor fusion**, including:

* Differential drive simulation  
* IMU + wheel odometry fusion via EKF  
* Drift reduction using filtered odometry  
* SLAM-based mapping  
* AMCL localization  
* Autonomous navigation with Nav2  

It serves as a structured reference implementation for developing robust mobile robot navigation systems in simulation before deploying to real hardware.
