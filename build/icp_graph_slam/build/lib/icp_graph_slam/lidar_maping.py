import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import csv
import time

class LaserScanToCSV(Node):
    def __init__(self):
        super().__init__('laserscan_to_csv')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.listener_callback,
            10)
        self.subscription
        
        self.odom_subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10)
        self.odom_subscription

        self.angle_min = []
        self.angle_max = []
        self.angle_increment = []
        self.range_min = []
        self.range_max = []
        self.ranges = []
        self.intensities = []
        self.poses = []
        self.latest_pose = None

    def listener_callback(self, msg):
        self.get_logger().info('Received LaserScan data')
        self.angle_min.append(msg.angle_min)
        self.angle_max.append(msg.angle_max)
        self.angle_increment.append(msg.angle_increment)
        self.range_min.append(msg.range_min)
        self.range_max.append(msg.range_max)
        self.ranges.append(list(msg.ranges))
        self.intensities.append(list(msg.intensities))
        self.poses.append(self.latest_pose)

    def odom_callback(self, msg):
        self.latest_pose = (
            msg.pose.pose.position.x,
            msg.pose.pose.position.y,
            self.get_yaw_from_quaternion(msg.pose.pose.orientation)
        )

    def get_yaw_from_quaternion(self, orientation):
        import math
        x, y, z, w = (
            orientation.x,
            orientation.y,
            orientation.z,
            orientation.w
        )
        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        yaw = math.atan2(siny_cosp, cosy_cosp)
        return yaw

def main():
    rclpy.init()
    node = LaserScanToCSV()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        csv_file = f'/home/ziczac/dev/skripsi_code/ros2_workspace/data_store/mapping/{time.strftime("%d-%m|%H:%M:%S", time.localtime())}.csv'
        with open(csv_file, mode='w') as file:
            writer = csv.writer(file)
            writer.writerow([
                'pose',
                'angle_min', 'angle_max', 'angle_increment', 
                'range_min', 'range_max', 'ranges', 'intensities',
            ])
            for i in range(len(node.angle_min)):
                writer.writerow([
                    node.poses[i], 
                    node.angle_min[i], node.angle_max[i], node.angle_increment[i], 
                    node.range_min[i], node.range_max[i], 
                    node.ranges[i], node.intensities[i],
                ])
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
