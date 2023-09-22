import rclpy
from rclpy.node import Node
import math
from tf2_ros import TransformBroadcaster
import numpy as np

from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
from robot_interfaces.msg import TickCount

def quaternion_from_euler(ai, aj, ak):
    ai /= 2.0
    aj /= 2.0
    ak /= 2.0
    ci = math.cos(ai)
    si = math.sin(ai)
    cj = math.cos(aj)
    sj = math.sin(aj)
    ck = math.cos(ak)
    sk = math.sin(ak)
    cc = ci*ck
    cs = ci*sk
    sc = si*ck
    ss = si*sk

    q = np.empty((4, ))
    q[0] = cj*sc - sj*cs
    q[1] = cj*ss + sj*cc
    q[2] = cj*cs - sj*sc
    q[3] = cj*cc + sj*ss

    return q

class OdomPublisher(Node):

    def __init__(self):
        super().__init__('odom_publisher')
        self.subscription = self.create_subscription(TickCount, 'encoder_ticks', self.listener_callback, 10)
        self.subscription  # prevent unused variable warning

        self.publisher_ = self.create_publisher(Odometry, 'odometry', 10)

        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.tf_broadcaster = TransformBroadcaster(self)

        self.left_ticks_current = 0
        self.right_ticks_current = 0
        self.left_ticks_previous = 0
        self.right_ticks_previous = 0
        self.time_current = self.get_clock().now()
        self.time_previous = self.get_clock().now()

        self.ticks_per_revolution = 696.5
        self.wheel_radius = 0.0675
        self.distance_per_tick = 2 * math.pi * self.wheel_radius / self.ticks_per_revolution # meters
        self.wheel_base = 0.262

        self.x = 0
        self.y = 0
        self.th = 0

    def listener_callback(self, msg):
        self.left_ticks_current = msg.left_wheel_tick_count
        self.right_ticks_current = msg.right_wheel_tick_count

    def timer_callback(self):
        self.time_current = self.get_clock().now()

        left_ticks_difference = self.left_ticks_current - self.left_ticks_previous
        if (left_ticks_difference < -10000):
            left_ticks_difference = left_ticks_difference + 65535
        elif(left_ticks_difference > 10000):
            left_ticks_difference = 0 - (65535 - left_ticks_difference)

        right_ticks_difference = self.right_ticks_current - self.right_ticks_previous
        if (right_ticks_difference < -10000):
            right_ticks_difference = right_ticks_difference + 65535
        elif(right_ticks_difference > 10000):
            right_ticks_difference = 0 - (65535 - right_ticks_difference)

        dt = (self.time_current - self.time_previous).nanoseconds / 1e9 # time in seconds
        omega_left = left_ticks_difference * self.distance_per_tick / dt
        omega_right = right_ticks_difference * self.distance_per_tick / dt
        vx = (omega_right + omega_left) / 2
        vth = (omega_right - omega_left) / self.wheel_base
        delta_x = (vx * math.cos(self.th)) * dt
        delta_y = (vx * math.sin(self.th)) * dt
        delta_th = vth * dt
        self.x += delta_x
        self.y += delta_y
        self.th += delta_th
        q = quaternion_from_euler(0, 0, self.th)

        # odom_transform = TransformStamped()
        # odom_transform.header.stamp = self.get_clock().now().to_msg()
        # odom_transform.header.frame_id = "odom"
        # odom_transform.child_frame_id = "base_link"
        # odom_transform.transform.translation.x = self.x
        # odom_transform.transform.translation.y = self.y
        # odom_transform.transform.translation.z = 0.0
        # odom_transform.transform.rotation.x = q[0]
        # odom_transform.transform.rotation.y = q[1]
        # odom_transform.transform.rotation.z = q[2]
        # odom_transform.transform.rotation.w = q[3]
        # self.tf_broadcaster.sendTransform(odom_transform)

        odom = Odometry()
        odom.header.stamp = self.get_clock().now().to_msg()
        odom.header.frame_id = "odom"
        odom.child_frame_id = "base_footprint"
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation.x = q[0]
        odom.pose.pose.orientation.y = q[1]
        odom.pose.pose.orientation.z = q[2]
        odom.pose.pose.orientation.w = q[3]
        odom.twist.twist.linear.x = vx
        odom.twist.twist.linear.y = 0.0
        odom.twist.twist.angular.z = vth
        self.publisher_.publish(odom)

        self.left_ticks_previous = self.left_ticks_current
        self.right_ticks_previous = self.right_ticks_current
        self.time_previous = self.time_current


def main(args=None):
    print('Publishing odometry...')
    rclpy.init(args=args)
    odom0 = OdomPublisher()
    rclpy.spin(odom0)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    odom0.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
