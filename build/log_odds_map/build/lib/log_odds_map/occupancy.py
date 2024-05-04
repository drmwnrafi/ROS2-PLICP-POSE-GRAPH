#!/usr/bin/env python

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry, OccupancyGrid
from sensor_msgs.msg import LaserScan
import tf2_ros as tf
from tf_transformations import quaternion_from_euler, euler_from_quaternion
from geometry_msgs.msg import TransformStamped
import math
import numpy as np
from math import sin, cos, pi, tan, atan2
from itertools import groupby
from operator import itemgetter
from log_odds_map.localmap import localmap


class OccupancyMapping(Node):
    def __init__(self):
        super().__init__('occupancy_mapping')
        self.create_subscription(Odometry, '/odom', self.odometry_callback, 10)
        self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.map_publisher = self.create_publisher(OccupancyGrid, '/map', 1)
        self.br = tf.TransformBroadcaster(self)

        self.pose = [0.0, 0.0, 0.0]
        self.pose_quat = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.height, self.width, self.resolution = 10, 10, 0.1
        self.map_origin = [self.width / 2.0, self.height / 2.0]
        self.local_map = localmap(self.height, self.width, self.resolution, self.map_origin)
        self.get_logger().info('---- Occupancy node started ----')

    def handle_robot_pose(self, parent, child, pose):
        t = TransformStamped()
        t.header.frame_id = parent
        t.child_frame_id = child
        t.header.stamp = self.get_clock().now().to_msg()
        t.transform.translation.x = -pose[0]
        t.transform.translation.y = -pose[1]
        t.transform.translation.z = 0.0
        q = quaternion_from_euler(0, 0, -pose[2])
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]
        self.br.sendTransform(t)

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

    def scan_callback(self, msg):
        scandata = msg.ranges
        angle_min = msg.angle_min
        angle_max = msg.angle_max
        angle_increment = msg.angle_increment
        range_min = msg.range_min
        range_max = msg.range_max

        if self.local_map:
            self.local_map.updatemap(scandata, angle_min, angle_max, angle_increment, range_min, range_max, self.pose)
            self.handle_robot_pose("map", "odom", self.pose)
            self.publish_map()

    def publish_map(self):
        msg = OccupancyGrid()
        msg.header.frame_id = 'map'
        msg.info.resolution = self.resolution
        msg.info.width = math.ceil(self.width / self.resolution)
        msg.info.height = math.ceil(self.height / self.resolution)
        msg.info.origin.position.x = -self.map_origin[0]
        msg.info.origin.position.y = -self.map_origin[1]
        map = np.array(self.local_map.localmap, dtype=np.int8).flatten().tolist()
        msg.data = map
        self.map_publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    occupancy_mapping = OccupancyMapping()
    rclpy.spin(occupancy_mapping)
    occupancy_mapping.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
