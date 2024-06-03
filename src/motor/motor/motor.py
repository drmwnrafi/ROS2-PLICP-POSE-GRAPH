import rclpy
from rclpy.node import Node
from wheel_interfaces.msg import WheelInfos 
from modules import ddsm115
import csv
from math import sin, cos, pi, radians, degrees
import time
from multiprocessing import Process
from nav_msgs.msg import Odometry
from tf_transformations import euler_from_quaternion


class MotorNode(Node):
    def __init__(self):
        super().__init__('motor')
        self.left_drive = ddsm115.MotorControl(device="/dev/ttyUSB0")
        self.right_drive = ddsm115.MotorControl(device="/dev/ttyUSB1")
        self.right_drive.set_drive_mode(_id=1, _mode=2)
        self.left_drive.set_drive_mode(_id=2, _mode=2)
        self.left_publisher = self.create_publisher(WheelInfos, 'left_wheel', 10)
        self.right_publisher = self.create_publisher(WheelInfos, 'right_wheel', 10)
        self.cmd_wheel = self.create_subscription(WheelInfos, 'wheel_cmd', self.get_wheel_command, 10)
        self.odom_sub = self.create_subscription(Odometry, "odom", self.odom_callback, 10)

        self.timer = self.create_timer(0.01, self.publish_values)
        self.timer_pid = self.create_timer(0.01, self.straight)

        self.wheel_distance = 0.283
        self.wheel_radius = 0.05

        self.prev_pos_l = None
        self.prev_pos_r = None

        self.then = self.get_clock().now()

        self.x = 0
        self.y = 0
        self.yaw = 0

        self.Kp = 9
        self.Ki = 0.0
        self.Kd = 6

        self.prev_error = 0.0
        self.integral = 0.0
        self.setpoint_yaw = None

        self.max_speed = 30

        self.rpm_cmd_left = 0
        self.rpm_cmd_right = 0

        self.get_logger().info('---- Motor node started ----')


    def send_rpm_parallel(self, id, rpm):
        if id == 1:
            self.right_drive.send_rpm(_id=1, rpm=rpm)
        elif id == 2:
            self.left_drive.send_rpm(_id=2, rpm=rpm)

    def publish_values(self):
        rpm_L, cur_L, pos_L = self.left_drive.get_motor_feedback(_id = 2)
        rpm_R, cur_R, pos_R = self.right_drive.get_motor_feedback(_id = 1)

        left_msg = WheelInfos()
        left_msg.rpm = int(rpm_L)
        left_msg.current = int(cur_L)
        left_msg.position = -pos_L
        self.left_publisher.publish(left_msg)

        right_msg = WheelInfos()
        right_msg.rpm = int(rpm_R)
        right_msg.current = int(cur_R)
        right_msg.position = int(pos_R)
        self.right_publisher.publish(right_msg)

    def get_wheel_command(self, msg):
        self.rpm_cmd_left = msg.cmd_value[0]
        self.rpm_cmd_right = msg.cmd_value[1]
        self.get_logger().info(f"RPM command for wheel: {msg.cmd_value}")
    
    def straight(self,):
        if -(self.rpm_cmd_left) == self.rpm_cmd_right and self.rpm_cmd_right != 0 and self.rpm_cmd_left != 0:
            if self.setpoint_yaw == None :
                self.setpoint_yaw = self.yaw
            new_left, new_right = self.pid(self.rpm_cmd_left, desired_yaw=self.setpoint_yaw)
            new_left = max(-self.max_speed, min(new_left, self.max_speed))
            new_right = max(-self.max_speed, min(new_right, self.max_speed))
            p1 = Process(target=self.send_rpm_parallel, args=(2, -new_left))
            p2 = Process(target=self.send_rpm_parallel, args=(1, new_right))
            p1.start()
            p2.start()
            p1.join()
            p2.join()
        else :
            self.setpoint_yaw = None
            p1 = Process(target=self.send_rpm_parallel, args=(2, self.rpm_cmd_left))
            p2 = Process(target=self.send_rpm_parallel, args=(1, self.rpm_cmd_right))
            p1.start()
            p2.start()
            p1.join()
            p2.join()

    def odom_callback(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        self.z = msg.pose.pose.position.z
        qx = msg.pose.pose.orientation.x
        qy = msg.pose.pose.orientation.y
        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w
        quaternion = [qx, qy, qz, qw]
        (_, _, self.yaw) = euler_from_quaternion(quaternion)

    def pid(self, base_rpm, desired_yaw):
        current_yaw = self.yaw
        error = desired_yaw - current_yaw
        P = self.Kp * error
        self.integral += error
        I = self.Ki * error
        derivative = (error - self.prev_error) / 1
        D = self.Kd * derivative
        output = P + I + D
        self.prev_error = error
        return int((base_rpm + output)), int((base_rpm - output))

def main():
    rclpy.init()
    motor_publisher = MotorNode()
    try:
        rclpy.spin(motor_publisher)
    except KeyboardInterrupt:
        rclpy.shutdown()

if __name__ == '__main__':
    main()
