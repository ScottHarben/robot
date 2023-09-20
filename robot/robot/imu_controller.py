import rclpy
from rclpy.node import Node
from math import pi

from sensor_msgs.msg import Imu

class ImuController(Node):

    def __init__(self):
        super().__init__('imu_controller')
        self.imu_subscription = self.create_subscription(Imu, 'camera/imu', self.listener_callback, 10)
        self.imu_subscription  # prevent unused variable warning

        self.publisher_ = self.create_publisher(Imu, 'imu/data_raw', 10)
        
        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.data_raw = Imu()
        self.message_recieved = False

    def listener_callback(self, msg):
        self.message_recieved = True
        self.data_raw.header.frame_id = msg.header.frame_id
        self.data_raw.header.stamp = msg.header.stamp
        self.data_raw.orientation.x = msg.orientation.x
        self.data_raw.orientation.y = msg.orientation.y
        self.data_raw.orientation.z = msg.orientation.z
        self.data_raw.orientation.w = msg.orientation.w
        self.data_raw.orientation_covariance = msg.orientation_covariance
        self.data_raw.angular_velocity.x = msg.angular_velocity.z
        self.data_raw.angular_velocity.y = msg.angular_velocity.x * -1.0
        self.data_raw.angular_velocity.z = msg.angular_velocity.y * -1.0
        self.data_raw.angular_velocity_covariance = msg.angular_velocity_covariance
        self.data_raw.linear_acceleration.x = msg.linear_acceleration.z
        self.data_raw.linear_acceleration.y = msg.linear_acceleration.x * -1.0
        self.data_raw.linear_acceleration.z = msg.linear_acceleration.y * -1.0
        self.data_raw.linear_acceleration_covariance = msg.linear_acceleration_covariance

    def timer_callback(self):
        if self.message_recieved:
            self.publisher_.publish(self.data_raw)


def main(args=None):
    print('Publishing imu/data_raw...')
    rclpy.init(args=args)
    imu_controller = ImuController()
    rclpy.spin(imu_controller)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    imu_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()