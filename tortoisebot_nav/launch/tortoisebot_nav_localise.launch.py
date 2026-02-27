from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution

def generate_launch_description(): 

    pkg_name ='tortoisebot_description'
    pkg_description=FindPackageShare(pkg_name) 

    rviz_file = 'slam_robot_bot.rviz'
    rviz_config_file=PathJoinSubstitution([pkg_description,'rviz',rviz_file])

    #RViz node 
    rviz_bot=Node(
        package='rviz2',
        name ='rviz2_bot',
		output  ='log',
        arguments =['-d', rviz_config_file],
        executable='rviz2',
	    parameters=[{
            'use_sim_time': True}]
     )
    
    twist_mux_config=PathJoinSubstitution([FindPackageShare('tortoisebot_nav'),'config','twist_mux.yaml'])

    twist_mux_node = Node(
    package='twist_mux',
    executable='twist_mux',
    name='twist_mux',
    parameters=[twist_mux_config,
                {'use_sim_time': True,
                 }],
    output='screen'
)
    nav_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [PathJoinSubstitution([FindPackageShare('tortoisebot_nav'),'launch','localization.launch.py'])]),
                                                            launch_arguments={'use_sim_time':'true'}.items()
                                                        )
    
    return LaunchDescription([
        rviz_bot,
        twist_mux_node,
        nav_launch
    ])