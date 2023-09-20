import rclpy
from rclpy.node import Node
import Jetson.GPIO as GPIO

from robot_interfaces.msg import DutyCycle


class MotorDriver(Node):

    def __init__(self):
        super().__init__('motor_driver')
        self.subscription = self.create_subscription(DutyCycle, 'duty_cycle', self.listener_callback, 10)
        self.subscription  # prevent unused variable warning

        self.pwm_pin_left = 32
        self.pwm_pin_right = 33

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.pwm_pin_left, GPIO.OUT)
        GPIO.setup(self.pwm_pin_right, GPIO.OUT)
        self.pwm_left = GPIO.PWM(self.pwm_pin_left, 100)
        self.pwm_right = GPIO.PWM(self.pwm_pin_right, 100)
        self.pwm_left.start(0)
        self.pwm_right.start(0)

        # #TODO:
        # #stop if no message recieved

    def listener_callback(self, msg):
        self.pwm_left.ChangeDutyCycle(msg.duty_cycle_left)
        self.pwm_right.ChangeDutyCycle(msg.duty_cycle_right)

def main(args=None):
    print('Running motor driver...')
    rclpy.init(args=args)
    motor_driver = MotorDriver()
    rclpy.spin(motor_driver)
    motor_driver.pwm_left.close()
    motor_driver.pwm_right.close()
    motor_driver.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()