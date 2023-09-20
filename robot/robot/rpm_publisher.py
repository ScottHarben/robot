import rclpy
from rclpy.node import Node

from robot_interfaces.msg import TickCount, WheelRPM


class RPMPublisher(Node):

    def __init__(self):
        super().__init__('rpm_publisher')
        self.subscription = self.create_subscription(TickCount, 'encoder_ticks', self.listener_callback, 10)
        self.subscription  # prevent unused variable warning

        self.publisher_ = self.create_publisher(WheelRPM, 'feedback_rpm', 10)
        
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.left_ticks_current = 0
        self.right_ticks_current = 0
        self.left_ticks_previous = 0
        self.right_ticks_previous = 0
        self.time_current = self.get_clock().now()
        self.time_previous = self.get_clock().now()

        self.ticks_per_revolution = 696.5
        self.rpm_to_radians = 0.10471975512
        self.wheel_radius = 0.0625

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

        delta_time = (self.time_current - self.time_previous).nanoseconds / 1e9 # time in seconds

        left_wheel_rpm = (left_ticks_difference / (delta_time * self.ticks_per_revolution)) * 60.0
        right_wheel_rpm = (right_ticks_difference / (delta_time * self.ticks_per_revolution)) * 60.0

        self.left_ticks_previous = self.left_ticks_current
        self.right_ticks_previous = self.right_ticks_current
        self.time_previous = self.time_current

        msg = WheelRPM()
        msg.rpm_left = left_wheel_rpm
        msg.rpm_right = right_wheel_rpm
        self.publisher_.publish(msg)


def main(args=None):
    print('Publishing feedback_rpm...')
    rclpy.init(args=args)
    rpm_publisher = RPMPublisher()
    rclpy.spin(rpm_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    rpm_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()