#!/usr/bin/env python

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry, OccupancyGrid
from sensor_msgs.msg import LaserScan
import tf2_ros as tf
from tf_transformations import quaternion_from_euler, euler_from_quaternion
from geometry_msgs.msg import TransformStamped
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
import math
import numpy as np
from math import sin, cos, pi, tan, atan2
from itertools import groupby
from operator import itemgetter
from log_odds_map.localmap import localmap

class BuildMap():
    pass

class OccupancyMapping(Node):
    def __init__(self):
        super().__init__('occupancy_mapping')
        self.create_subscription(Odometry, '/odom', self.odometry_callback, 10)
        self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.map_publisher = self.create_publisher(OccupancyGrid, '/map', 1)
        self.padding = 5
        self.max_width = 0
        self.max_height = 0

        self.pose = [0.0, 0.0, 0.0]
        self.resolution = 0.1
        self.get_logger().info('---- Occupancy node started ----')

        self.tf_static = StaticTransformBroadcaster(self)
        t = TransformStamped()
        t.header.frame_id = 'map'
        t.child_frame_id = 'odom'
        t.header.stamp = self.get_clock().now().to_msg()
        t.transform.translation.x = 0.0
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.0
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 0.0
        self.tf_static.sendTransform(t)

    def odometry_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        q0 = msg.pose.pose.orientation.w
        q1 = msg.pose.pose.orientation.x
        q2 = msg.pose.pose.orientation.y
        q3 = msg.pose.pose.orientation.z
        q = [q0, q1, q2, q3]
        _, _, theta = euler_from_quaternion(q)
        self.pose = [x, y, theta]

    def polar_to_cartesian(self, scans, range_max, range_min, angle_min, angle_increment):
        x = []
        y = [] 
        for i in range(len(scans)):
            if range_min < scans[i] < range_max:
                angle = angle_min + i * angle_increment 
                px = int(self.pose[0] + (scans[i]) * cos(angle))
                py = int(self.pose[1] + (scans[i]) * sin(angle))
                x.append(px)
                y.append(py)
        return np.array([x, y])

    def scan_callback(self, msg):
        scandata = msg.ranges
        angle_min = msg.angle_min
        angle_max = msg.angle_max
        angle_increment = msg.angle_increment
        range_min = msg.range_min
        range_max = msg.range_max

        cartesian = self.polar_to_cartesian(scandata, range_max, range_min, angle_min, angle_increment)
        max_cart = [max(cartesian[0]), max(cartesian[1])]
        
        self.publish_map(max_cart)

    def publish_map(self, max_point):
        msg = OccupancyGrid()
        msg.header.frame_id = 'map'
        msg.info.resolution = self.resolution

        width = max_point[1] 
        height = max_point[0] 
        if width > self.max_width :
            self.max_width = width
        elif height > self.max_height :
            self.max_height = height

        msg.info.width = math.ceil(self.max_width / self.resolution)
        msg.info.height = math.ceil(self.max_height / self.resolution)
        msg.info.origin.position.x = 0.0
        msg.info.origin.position.y = -self.max_height/2
        map_size = int(msg.info.width * msg.info.height)
        map_publish = np.full(map_size, -1, dtype=np.int8).tolist()
        print(len(map_publish), "||||", map_size)
        msg.data = map_publish
        self.map_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    occupancy_mapping = OccupancyMapping()
    rclpy.spin(occupancy_mapping)
    occupancy_mapping.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()