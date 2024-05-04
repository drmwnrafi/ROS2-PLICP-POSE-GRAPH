import rclpy
from rclpy.node import Node
from math import sin, cos, pi, radians, degrees
import numpy as np

from geometry_msgs.msg import Quaternion, TransformStamped, Twist
from nav_msgs.msg import Odometry
from wheel_interfaces.msg import WheelInfos
from tf2_ros import TransformBroadcaster


class DifferentialDrive(Node):
    def __init__(self):
        super().__init__('diff_tf')
        self.get_logger().info('---- diff_tf node started ----')

        self.rate_hz = self.declare_parameter('rate_hz', 10.0).value
        self.create_timer(1.0 / self.rate_hz, self.update)

        self.wheel_distance = 0.283
        self.wheel_radius = 0.05

        self.base_frame_id = self.declare_parameter('base_frame_id', 'base_link').value
        self.odom_frame_id = self.declare_parameter('odom_frame_id', 'odom').value

        self.pos_l = None
        self.pos_r = None
        self.prev_pos_l = None
        self.prev_pos_r = None
        self.dist_left = 0
        self.dist_right = 0
        
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.linear = 0.0
        self.angular = 0.0
        self.check = 0.0
        self.then = self.get_clock().now()

        self.create_subscription(WheelInfos, 'left_wheel', self.left_wheel_msg, 10)
        self.create_subscription(WheelInfos, 'right_wheel', self.right_wheel_msg, 10)
        self.odom_publish = self.create_publisher(Odometry, 'odom', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

    def update(self):
        now = self.get_clock().now()
        time_elapsed = now - self.then
        self.then = now
        time_elapsed = time_elapsed.nanoseconds / 1e9

        if self.prev_pos_l is not None:
            d_theta_L = self.difference_between_angles(self.prev_pos_l, self.pos_l)
            self.dist_left = (pi * 2 * self.wheel_radius * (d_theta_L / 360))
            self.prev_pos_l = self.pos_l
        else:
            self.prev_pos_l = self.pos_l
        if self.prev_pos_r is not None:
            d_theta_R = self.difference_between_angles(self.prev_pos_r, self.pos_r)
            self.dist_right = (pi * 2 * self.wheel_radius * (d_theta_R / 360))
            self.prev_pos_r = self.pos_r
        else:
            self.prev_pos_r = self.pos_r

        d_distance = (self.dist_left + self.dist_right) * 0.5
        d_theta = (self.dist_right - self.dist_left) / self.wheel_distance

        self.linear = d_distance
        self.angular = d_theta

        # if abs(self.dist_left - self.dist_right) < 1e-6:
        #     d_theta = 0
        #     dx = d_distance
        #     dy = 0
        # else:
        #     icc_radius = d_distance / d_theta
        #     if abs(icc_radius) < 1e-6:
        #         d_theta = (2 * self.dist_right) / icc_radius
        #         dx = 0
        #         dy = 0
        #     else:
        #         d_theta = d_distance / icc_radius
        #         dx = icc_radius * sin(d_theta)
        #         dy = - (icc_radius * cos(d_theta) - 1)
        
        odom_dx = d_distance * cos(self.theta + d_theta/2)
        odom_dy = d_distance * sin(self.theta + d_theta/2)

        # self.x = self.x + (cos(self.theta) * odom_dx - sin(self.theta) * odom_dx)
        # self.y = self.y + (sin(self.theta) * odom_dy + cos(self.theta) * odom_dy)

        self.x += odom_dx
        self.y += odom_dy
        self.theta = (self.theta + d_theta) % (2 * pi)

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

    def difference_between_angles(self, first_angle, second_angle):
        return (second_angle - first_angle + 180) % 360 - 180

    def left_wheel_msg(self, msg):
        self.pos_l = msg.position

    def right_wheel_msg(self, msg):
        self.pos_r = msg.position


def main(args=None):
    rclpy.init(args=args)
    diff_tf = DifferentialDrive()
    try:
        rclpy.spin(diff_tf)
    except KeyboardInterrupt:
        pass

    diff_tf.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()