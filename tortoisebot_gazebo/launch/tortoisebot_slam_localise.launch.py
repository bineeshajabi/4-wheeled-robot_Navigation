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
		 executable ='rviz2',
		 name       ='rviz2_bot',
		 output     ='log',
		 arguments  =['-d', rviz_config_file],
         parameters =[{'use_sim_time': True}])

    slam_map_l =PathJoinSubstitution([FindPackageShare('tortoisebot_gazebo'),'config','mapper_localization.yaml'])
    #Slam_toolbox
    slam_launch_l = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [PathJoinSubstitution([FindPackageShare('slam_toolbox'),'launch','localization_launch.py'])]),
                                                            launch_arguments={'slam_params_file':slam_map_l,
                                                                              'use_sim_time':'true'}.items()
                                                        )
    
    return LaunchDescription([
        rviz_bot,
        slam_launch_l
    ])