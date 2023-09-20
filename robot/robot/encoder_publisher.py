import rclpy
from rclpy.node import Node
import Jetson.GPIO as GPIO
from robot_interfaces.msg import TickCount


class EncoderPublisher(Node):

    def __init__(self):
        super().__init__('encoder_publisher')
        self.encoder_ticks_left_subscription = self.create_subscription(TickCount, 'encoder_ticks_left', self.listener_callback_left, 10)
        self.encoder_ticks_left_subscription  # prevent unused variable warning

        self.encoder_ticks_right_subscription = self.create_subscription(TickCount, 'encoder_ticks_right', self.listener_callback_right, 10)
        self.encoder_ticks_right_subscription  # prevent unused variable warning
        
        self.publisher_ = self.create_publisher(TickCount, 'encoder_ticks', 10)
        
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        self.encoder_ticks_left = 0
        self.encoder_ticks_right = 0

    def listener_callback_left(self, msg):
        self.encoder_ticks_left = msg.left_wheel_tick_count
    
    def listener_callback_right(self, msg):
        self.encoder_ticks_right = msg.right_wheel_tick_count

    def timer_callback(self):
        msg = TickCount()
        msg.left_wheel_tick_count = self.encoder_ticks_left
        msg.right_wheel_tick_count = self.encoder_ticks_right
        self.publisher_.publish(msg)


def main(args=None):
    print('Publishing encoder_ticks...')
    rclpy.init(args=args)
    encoder_publisher = EncoderPublisher()
    rclpy.spin(encoder_publisher)
    GPIO.cleanup()

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    encoder_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
