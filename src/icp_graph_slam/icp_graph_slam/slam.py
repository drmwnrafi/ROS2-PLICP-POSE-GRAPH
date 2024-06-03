import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import csv

class ICPSLAM():
    def __init__(self) -> None:
        pass
    
    def polar_to_cartesian():
        pass

class Lidar(Node):
    def __init__(self):
        super().__init__('wheeltec_n10')
        self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.ranges = []
        self.angel_min = []
        self.angel_max = []
        self.increment = []
        self.ranges_min = []
        self.ranges_max = []

    def scan_callback(self, msg):
        scandata = msg.ranges
        angle_min = msg.angle_min
        angle_max = msg.angle_max
        angle_increment = msg.angle_increment
        range_min = msg.range_min
        range_max = msg.range_max
        
        self.ranges.append(scandata)
        self.angel_min.append(angle_min)
        self.angel_max.append(angle_max)
        self.increment.append(angle_increment)
        self.ranges_min.append(range_min)
        self.ranges_max.append(range_max)

def main():
    rclpy.init()
    lidar_subs = Lidar()
    try:
        rclpy.spin(lidar_subs)
    except KeyboardInterrupt:
            file_path = '/home/ziczac/dev/skripsi_code/ros2_workspace/data_store/lidar_data/2.csv'
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['angel_min', 'angle_max', 'increment', 'ranges_min', 'ranges_max', 'ranges',])
                for i in range(len(lidar_subs.ranges)):
                    writer.writerow([
                        lidar_subs.angel_min[i],
                        lidar_subs.angel_max[i],
                        lidar_subs.increment[i],
                        lidar_subs.ranges_min[i],
                        lidar_subs.ranges_max[i],
                        lidar_subs.ranges[i],
                    ])
    rclpy.shutdown()

    