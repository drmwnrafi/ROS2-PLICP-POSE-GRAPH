import rclpy
from rclpy.node import Node
from math import sin, cos, pi, radians, degrees
import numpy as np
import csv
import time
from geometry_msgs.msg import Quaternion, TransformStamped, Twist
from nav_msgs.msg import Odometry
from wheel_interfaces.msg import WheelInfos
from tf2_ros import TransformBroadcaster


class DifferentialDrive(Node):
    def __init__(self):
        super().__init__('diff_tf')
        self.get_logger().info('---- diff_tf node started ----')

        self.rate_hz = self.declare_parameter('rate_hz', 100.0).value
        self.create_timer(1.0 / self.rate_hz, self.update)

        self.wheel_distance = 0.283
        self.wheel_radius = 0.05

        self.base_frame_id = self.declare_parameter('base_frame_id', 'base_link').value
        self.odom_frame_id = self.declare_parameter('odom_frame_id', 'odom').value

        self.pos_l = None
        self.pos_r = None
        self.prev_pos_l = None
        self.prev_pos_r = None
        self.dist_left_pos = 0
        self.dist_right_pos = 0

        self.rpm_l = None
        self.rpm_r = None
        self.dist_left_rpm = 0
        self.dist_right_rpm = 0
        
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.linear = 0.0
        self.angular = 0.0
        self.check = 0.0
        self.then = self.get_clock().now()
        
        self.rpm_l_store = []
        self.rpm_r_store = []
        self.pos_l_store = []
        self.pos_r_store = []
        self.pose = []
        self.time_stamp = []

        self.create_subscription(WheelInfos, 'left_wheel', self.left_wheel_msg, 10)
        self.create_subscription(WheelInfos, 'right_wheel', self.right_wheel_msg, 10)
        self.odom_publish = self.create_publisher(Odometry, 'odom', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

    def difference_between_angles(self, first_angle, second_angle):
        return (second_angle - first_angle + 180) % 360 - 180

    def distance_pos(self, pos_l, pos_r):
        if self.prev_pos_l is not None:
            d_theta_L = self.difference_between_angles(self.prev_pos_l, pos_l)
            self.dist_left_pos = (pi * 2 * self.wheel_radius * (d_theta_L / 360))
            self.prev_pos_l = pos_l
        else:
            self.prev_pos_l = pos_l
        if self.prev_pos_r is not None:
            d_theta_R = self.difference_between_angles(self.prev_pos_r, pos_r)
            self.dist_right_pos = (pi * 2 * self.wheel_radius * (d_theta_R / 360))
            self.prev_pos_r = pos_r
        else:
            self.prev_pos_r = pos_r

    def distance_rpm(self, rpm_l, rpm_r, delta_t):
        d_left_rpm = ((rpm_l/60) * 2 * pi * self.wheel_radius) * delta_t # meter
        d_right_rpm = ((rpm_r/60) * 2 * pi * self.wheel_radius) * delta_t # meter
        
        self.dist_left_rpm += d_left_rpm
        self.dist_right_pos_rpm += d_right_rpm 

    def update(self):
        now = self.get_clock().now()
        time_elapsed = now-self.then

        self.distance_pos(self.pos_l, self.pos_r)
        d_distance = (self.dist_left_pos + self.dist_right_pos) * 0.5
        d_theta = (self.dist_right_pos - self.dist_left_pos) / self.wheel_distance

        self.linear = d_distance
        self.angular = d_theta
        
        odom_dx = d_distance * cos(self.theta + d_theta/2)
        odom_dy = d_distance * sin(self.theta + d_theta/2)

        self.x += odom_dx
        self.y += odom_dy
        self.theta = (self.theta + d_theta) % (2 * pi)

        self.rpm_l_store.append(self.rpm_l)
        self.rpm_r_store.append(self.rpm_r)
        self.pos_l_store.append(self.pos_l)
        self.pos_r_store.append(self.pos_r)
        self.time_stamp.append(now)
        self.pose.append([self.x, self.y, self.theta])

        quaternion = Quaternion()
        quaternion.x = 0.0
        quaternion.y = 0.0
        quaternion.z = np.sin(self.theta / 2)
        quaternion.w = np.cos(self.theta / 2)

        tf_stamped_msg = TransformStamped()
        tf_stamped_msg.header.stamp = now.to_msg()
        tf_stamped_msg.header.frame_id = self.odom_frame_id 
        tf_stamped_msg.child_frame_id = self.base_frame_id
        tf_stamped_msg.transform.translation.x = self.x
        tf_stamped_msg.transform.translation.y = self.y
        tf_stamped_msg.transform.translation.z = 0.0
        tf_stamped_msg.transform.rotation = quaternion

        self.tf_broadcaster.sendTransform(tf_stamped_msg)

        odom = Odometry()
        odom.header.stamp = now.to_msg()
        odom.header.frame_id = self.odom_frame_id
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation = quaternion
        odom.child_frame_id = self.base_frame_id
        odom.twist.twist.linear.x = self.linear
        odom.twist.twist.linear.y = 0.0
        odom.twist.twist.angular.z = self.angular
        self.odom_publish.publish(odom)
        self.then = now

    def left_wheel_msg(self, msg):
        self.pos_l = msg.position
        self.rpm_l = msg.rpm

    def right_wheel_msg(self, msg):
        self.pos_r = msg.position
        self.rpm_r = msg.rpm


def main(args=None):
    rclpy.init(args=args)
    diff_tf = DifferentialDrive()
    try:
        rclpy.spin(diff_tf)
    except KeyboardInterrupt as e:
        print(e)
        # file_path = f'/home/ziczac/dev/skripsi_code/ros2_workspace/data_store/20rpm/{time.strftime("%d-%m|%H:%M:%S", time.localtime())}.csv'
        # with open(file_path, mode='w', newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerow(
        #         ['RPM_Left', 
        #          'RPM_Right',
        #          'Pos_Left',
        #          'Pos_Right',
        #          'Pose',
        #          'time_stamp'])
        #     for i in range(len(diff_tf.rpm_l_store)):
        #         writer.writerow([
        #             diff_tf.rpm_l_store[i],
        #             diff_tf.rpm_r_store[i],
        #             diff_tf.pos_l_store[i],
        #             diff_tf.pos_r_store[i],
        #             diff_tf.pose[i],
        #             diff_tf.time_stamp[i],
        #         ])

    diff_tf.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()