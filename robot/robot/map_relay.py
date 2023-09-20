import rclpy
from rclpy.node import Node

from nav_msgs.msg import OccupancyGrid

class MapRelay(Node):

    def __init__(self):
        super().__init__('map_relay')
        self.rtabmap_map_subscription = self.create_subscription(OccupancyGrid, 'rtabmap/map', self.listener_callback, 10)
        self.rtabmap_map_subscription  # prevent unused variable warning

        self.publisher_ = self.create_publisher(OccupancyGrid, 'map', 10)
        
        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.data_raw = OccupancyGrid()
        self.message_recieved = False

    def listener_callback(self, msg):
        self.message_recieved = True
        self.data_raw = msg

    def timer_callback(self):
        if self.message_recieved:
            self.publisher_.publish(self.data_raw)


def main(args=None):
    print('Relaying rtabmap/map to map...')
    rclpy.init(args=args)
    map_relay = MapRelay()
    rclpy.spin(map_relay)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    map_relay.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()