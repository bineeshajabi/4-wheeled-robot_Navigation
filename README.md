4-Wheeled Robot Navigation with Sensor Fusion (ROS 2 & Gazebo)
Overview

This repository demonstrates a complete 4-wheeled differential drive robot simulation using ROS 2 and Gazebo. It includes:

Differential drive simulation

LiDAR and IMU integration

Sensor fusion using robot_localization

SLAM-based mapping

AMCL localization

Autonomous navigation using Nav2

The system implements a full mobile robotics pipeline:

Robot Model → Gazebo → Sensor Fusion → SLAM/Localization → Nav2 → Autonomous Navigation

Repository Structure
4-wheeled-robot_Navigation/
├── tortoisebot_description/   # URDF and robot_state_publisher launch
├── tortoisebot_gazebo/        # Gazebo world and spawn launch files
├── tortoisebot_nav/           # SLAM, localization, navigation configs

Note: The robot model is defined entirely using URDF/Xacro. No external mesh files are used.

System Architecture
High-Level Flow

URDF/Xacro defines robot structure and joints

Gazebo simulates:

Differential drive motion

Wheel odometry

IMU

LiDAR

robot_localization performs sensor fusion

SLAM builds a map

AMCL localizes the robot

Nav2 performs global and local planning

Phase 1 — Robot Description (tortoisebot_description)
Purpose

Defines the physical robot model using URDF.

Robot Model Includes

Base chassis

Four wheels

Differential drive joints

LiDAR sensor

IMU sensor

Each link contains:

Inertial properties (mass & inertia)

Visual geometry

Collision geometry

Proper inertia and collision configuration are critical for stable simulation behavior.

Phase 2 — Gazebo Simulation (tortoisebot_gazebo)
Purpose

Handles physics simulation, wheel control, and sensor data generation.

Differential Drive

The robot uses a differential drive controller:

Left wheels grouped

Right wheels grouped

Controlled via /cmd_vel

Published topics:

/odom
/tf
Simulated Sensors
LiDAR

Publishes:

/scan

Used by:

SLAM

AMCL

Nav2 costmaps

IMU

Publishes:

/imu/data

Used for orientation estimation and sensor fusion.

Phase 3 — Sensor Fusion (Drift Reduction)
Why Sensor Fusion?

Raw wheel odometry suffers from:

Drift over time

Accumulated integration error

Wheel slippage

To reduce drift, the system integrates robot_localization.

Extended Kalman Filter (EKF)

The EKF fuses:

Wheel odometry (/odom)

IMU data (/imu/data)

It outputs:

/odometry/filtered
Benefits

Reduced drift

Improved pose estimation

Stabilized localization

Cleaner input for SLAM and Nav2

Frame Structure

Typical frame setup:

map → Global reference frame

odom → Continuous but drifting frame

base_link → Robot body frame

Filtered odometry improves the consistency of the odom → base_link transform.

Phase 4 — SLAM (Mapping Mode)

SLAM builds a 2D occupancy grid map.

Inputs

/scan

/odometry/filtered

Output
/map

Save the generated map:

ros2 run nav2_map_server map_saver_cli -f my_map
Phase 5 — Localization

Localization uses:

Map Server

AMCL

Lifecycle Manager

AMCL uses:

Laser scan data

Filtered odometry

This ensures stable pose estimation on the saved map.

Phase 6 — Autonomous Navigation

Start navigation:

ros2 launch tortoisebot_nav navigation_launch.py

Using RViz2, you can:

Set a 2D goal pose

Visualize the global path

Observe local costmaps

Monitor robot movement

Navigation Flow

Goal set in RViz

Global planner computes path

Local planner avoids obstacles

/cmd_vel commands sent

Robot moves in Gazebo

TF Tree 

ros2 run tf2_tools view_frames
