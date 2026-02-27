from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument,IncludeLaunchDescription,RegisterEventHandler, TimerAction
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from launch.event_handlers import OnProcessExit
from launch.substitutions import Command,PathJoinSubstitution,LaunchConfiguration
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory


def generate_launch_description(): 
    
    pkg_name ='tortoisebot_description'
    urdf_file='robot_model.urdf.xacro'

    rviz_file = 'slam_robot_bot.rviz'

    pkg_description=FindPackageShare(pkg_name) 

    use_sim_time = LaunchConfiguration('use_sim_time')

    # Initialization of directories
    xacro_file_GZ =PathJoinSubstitution([pkg_description,'urdf',urdf_file]) 

    #Robot description
    robot_description=ParameterValue(Command([
          'xacro',' ',xacro_file_GZ]),
          value_type=str)
    
    #Define the controllers used
    robot_controller= PathJoinSubstitution([FindPackageShare('tortoisebot_nav'), 'config', 'drive_controller.yaml'])

    rviz_config_file=PathJoinSubstitution([pkg_description,'rviz',rviz_file])

              
    #Declaration of Gazebo and world

    #Declare the world file
    world_file_name = 'obstacle_world.sdf'
    world = os.path.join(get_package_share_directory('tortoisebot_nav'), 'world', world_file_name)
    
    #Declare Gazebo launch arguments
    declare_gz_args_cmd = DeclareLaunchArgument(
          name = 'gz_args',
          default_value = ['-r -v 4 ',world],
          description = 'Defining the world for robot model'
     )
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='true',
        description='Uses simulated clock when set to true'
    )

    #Define launch arguments for intial pose
    x_args =  DeclareLaunchArgument('x', default_value='0.0', description='Initial X position of the robot')
    y_args =  DeclareLaunchArgument('y', default_value='0.0', description='Initial Y position of the robot')
    z_args =  DeclareLaunchArgument('z', default_value='0.0', description='Initial Z position of the robot')
    roll_args =  DeclareLaunchArgument('R', default_value='0.0', description='Initial Roll orientation of the robot')
    pitch_args =  DeclareLaunchArgument('P', default_value='0.0', description='Initial Pitch orientation of the robot')
    yaw_args =  DeclareLaunchArgument('Y', default_value='0.0', description='Initial Yaw orientation of the robot')

    #Launch configuration variables
    gz_args = LaunchConfiguration('gz_args')

    x=LaunchConfiguration('x')
    y=LaunchConfiguration('y')
    z=LaunchConfiguration('z')
    R=LaunchConfiguration('R')
    P=LaunchConfiguration('P')
    Y=LaunchConfiguration('Y')

    #Combined all together creating the gazebo node
    gazebo_launch = IncludeLaunchDescription(
          PythonLaunchDescriptionSource(
               [PathJoinSubstitution([FindPackageShare('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'])
               ]),
                launch_arguments={'gz_args': gz_args}.items())
    
    #Spawn the robot
    spawn_entity_robot=Node(
        package='ros_gz_sim',
        executable='create',
        arguments   = ['-topic', 'robot_description' , '-name', 'tortoisebot',
                       'x', x, 'y', y, 'z', z,
                       'R', R, 'P', P, 'Y', Y,'-z', '0.5'],
        output='screen'
     )
    # Bridge
    bridge_param=PathJoinSubstitution([FindPackageShare('tortoisebot_nav'), 'config', 'gz_bridge.yaml'])

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': bridge_param
            }],
        output='screen'
    )


    # Robot State Publisher to generate the /robot state topic with URDF data
    robot_state_publisher_bot=Node(
		package='robot_state_publisher',
		executable='robot_state_publisher',
		name='robot_state_publisher_bot',
		output='screen',
		parameters=[{
            'use_sim_time': use_sim_time,
			'robot_description':robot_description}]
     )
    
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )

    robot_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "diffDrive_controller",
            "--param-file",
            robot_controller,
            "--controller-ros-args",
            "-r /diffDrive_controller/cmd_vel:=/cmd_vel"            
        ],
    )

    ekf_node = Node(
        package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[{os.path.join(get_package_share_directory("tortoisebot_nav"), 'config', 'ekf.yaml')},
                        {'use_sim_time': True,
                         }]        
    )

    #RViz ode 
    #rviz_bot=Node(
	#	 executable ='rviz2',
	#	 output     ='log',
	#	 arguments  =['-d', rviz_config_file])

    #can be written as:
    #remappings=[('/diffDrive_controller/cmd_vel', '/cmd_vel')]
    
    
    return LaunchDescription([   
          declare_gz_args_cmd,
          declare_use_sim_time_cmd,
          x_args,y_args,z_args,roll_args,pitch_args,yaw_args,
          bridge,
          gazebo_launch,
          robot_state_publisher_bot,
          spawn_entity_robot,
          joint_state_broadcaster_spawner,
          robot_controller_spawner,
                  ])