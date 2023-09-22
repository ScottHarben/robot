import rclpy
from rclpy.node import Node
import math
from numpy import interp
from simple_pid import PID

from robot_interfaces.msg import DutyCycle, WheelRPM


class PidController(Node):

    def __init__(self):
        super().__init__('pid_controller')
        self.target_velocity_subscription = self.create_subscription(WheelRPM, 'target_rpm', self.target_rpm_callback, 10)
        self.target_velocity_subscription  # prevent unused variable warning

        self.feedback_velocity_subscription = self.create_subscription(WheelRPM, 'feedback_rpm', self.feedback_rpm_callback, 10)
        self.feedback_velocity_subscription  # prevent unused variable warning

        self.publisher_ = self.create_publisher(DutyCycle, 'duty_cycle', 10)
        
        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.feedback_rpm_left = 0.0
        self.feedback_rpm_right = 0.0

        self.max_rpm = 60.0
        self.wheel_diameter = 0.125
        self.duty_cycle_left = 0.0
        self.duty_cycle_right = 0.0

        # Kp = 0.1
        # Ki = 3.0
        # Kd = 0.0
        # output_limit = self.max_rpm # max mps to avoid runaway pid output
        # self.pid_left = PID(Kp, Ki, Kd, setpoint=0)
        # self.pid_left.output_limits = (0.0 - output_limit, output_limit)
        # self.pid_right = PID(Kp, Ki, Kd, setpoint=0)
        # self.pid_right.output_limits = (0.0 - output_limit, output_limit)

    def feedback_rpm_callback(self, msg):
        self.feedback_rpm_left = msg.rpm_left
        self.feedback_rpm_right = msg.rpm_right

    def target_rpm_callback(self, msg):
        # self.pid_left.setpoint = msg.rpm_left
        # self.pid_right.setpoint = msg.rpm_right
        # pid_rpm_left = self.pid_left(self.feedback_rpm_left)
        # pid_rpm_right = self.pid_right(self.feedback_rpm_right)
        # percentage_left = (pid_rpm_left / self.max_rpm) * 100.0
        # percentage_right = (pid_rpm_right / self.max_rpm) * 100.0

        #print("setpoint L {0} R {1} actual L {2} R {3}".format(round(msg.rpm_left, 2), round(msg.rpm_right, 2),round(pid_rpm_left, 2), round(pid_rpm_right, 2)))
        
        percentage_left = (msg.rpm_left / self.max_rpm) * 100.0
        percentage_right = (msg.rpm_right / self.max_rpm) * 100.0
        self.duty_cycle_left = interp(percentage_left, [-100, 100], [10.50, 19.50])
        self.duty_cycle_right = interp(percentage_right, [-100, 100], [10.50, 19.50])        

    def timer_callback(self):
        msg = DutyCycle()
        msg.duty_cycle_left = self.duty_cycle_left
        msg.duty_cycle_right = self.duty_cycle_right
        self.publisher_.publish(msg)


def main(args=None):
    print('Publishing duty_cycle...')
    rclpy.init(args=args)
    pid_controller = PidController()
    rclpy.spin(pid_controller)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    pid_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()