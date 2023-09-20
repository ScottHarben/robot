import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.substitutions import FindPackageShare
import launch
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution

def generate_launch_description():

    #lidar
    serial_port = LaunchConfiguration('serial_port', default='/dev/ttyUSB0')
    serial_baudrate = LaunchConfiguration('serial_baudrate', default='115200') #for A1/A2 is 115200
    frame_id = LaunchConfiguration('frame_id', default='laser')
    inverted = LaunchConfiguration('inverted', default='false')
    angle_compensate = LaunchConfiguration('angle_compensate', default='true')

    return launch.LaunchDescription([
        
        #lidar
        DeclareLaunchArgument(
            'serial_port',
            default_value=serial_port,
            description='Specifying usb port to connected lidar'),

        DeclareLaunchArgument(
            'serial_baudrate',
            default_value=serial_baudrate,
            description='Specifying usb port baudrate to connected lidar'),
        
        DeclareLaunchArgument(
            'frame_id',
            default_value=frame_id,
            description='Specifying frame_id of lidar'),

        DeclareLaunchArgument(
            'inverted',
            default_value=inverted,
            description='Specifying whether or not to invert scan data'),

        DeclareLaunchArgument(
            'angle_compensate',
            default_value=angle_compensate,
            description='Specifying whether or not to enable angle_compensate of scan data'),

        Node(
            package='rplidar_ros2',
            executable='rplidar_node',
            name='rplidar_scan_publisher',
            parameters=[{'serial_port': serial_port, 
                         'serial_baudrate': serial_baudrate, 
                         'frame_id': frame_id,
                         'inverted': inverted, 
                         'angle_compensate': angle_compensate}],
            output='screen'),

        #robot
        Node(
            package='robot',
            executable='encoder_publisher_left'),

        Node(
            package='robot',
            executable='encoder_publisher_right'),

        Node(
            package='robot',
            executable='encoder_publisher'),

        Node(
            package='robot',
            executable='rpm_publisher'),

        Node(
            package='robot',
            executable='motor_controller'),

        Node(
            package='robot',
            executable='pid_controller'),

        Node(
            package='robot',
            executable='motor_driver'),

        Node(
            package='robot',
            executable='odom_publisher')

  ])
