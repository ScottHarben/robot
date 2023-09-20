import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.substitutions import FindPackageShare
import launch
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution

def generate_launch_description():

    return launch.LaunchDescription([

        #imu
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('realsense2_camera'),
                    'launch',
                    'rs_launch.py'
                ])
            ]),
            launch_arguments={
                'enable_accel': 'true',
                'enable_gyro': 'true',
                'unite_imu_method': '1',
                'enable_rgbd': 'true',
                'align_depth.enable': 'true',
                'enable_sync': 'true',
                'enable_color': 'true',
                'enable_depth': 'true'     
                }.items()
        ),

        Node(
            package='robot',
            executable='imu_controller'),
        
        Node(
            package = "imu_filter_madgwick",
            executable="imu_filter_madgwick_node",
            name="imu_filter",
            output="screen",
            parameters=[os.path.join(
                        get_package_share_directory('robot_bringup'),
                        'config',
                        'imu_filter_madgwick_params.yaml')]),

        #robot localization
        Node(
            package = "robot_localization",
            executable="ekf_node",
            name="ekf_filter_node",
            output="screen",
            parameters=[os.path.join(
                        get_package_share_directory('robot_bringup'),
                        'config',
                        'ekf_params.yaml')]),

        # Node(
        #     package = "depthimage_to_laserscan",
        #     executable="depthimage_to_laserscan_node",
        #     name="depthimage_to_laserscan",
        #     output="screen",
        #     remappings=[
        #     ('/depth', '/camera/depth/image_rect_raw'),
        #     ('/depth_camera_info', '/camera/depth/camera_info')]),

        # Node(
        #     package='robot',
        #     executable='map_relay'),
  
  ])