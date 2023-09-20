from setuptools import setup

package_name = 'robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='scott',
    maintainer_email='scottharben@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'encoder_publisher_left = robot.encoder_publisher_left:main',
            'encoder_publisher_right = robot.encoder_publisher_right:main',
            'encoder_publisher = robot.encoder_publisher:main',
            'rpm_publisher = robot.rpm_publisher:main',
            'motor_controller = robot.motor_controller:main',
            'pid_controller = robot.pid_controller:main',
            'motor_driver = robot.motor_driver:main',
            'odom_publisher = robot.odom_publisher:main',
            'imu_controller = robot.imu_controller:main',
        ],
    },
)
