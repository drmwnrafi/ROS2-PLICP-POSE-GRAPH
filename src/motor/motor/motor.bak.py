import rclpy
from rclpy.node import Node
from wheel_interfaces.msg import WheelInfos 
from modules import ddsm115
import csv
from math import sin, cos, pi, radians, degrees
import math
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

        self.dist_left_pos = 0
        self.dist_right_pos = 0
        self.d_left_rpm = 0
        self.d_right_rpm = 0

        self.then = self.get_clock().now()

        self.x = 0
        self.y = 0
        self.yaw = 0

        self.rpm_l_store = []
        self.rpm_r_store = []
        self.pos_l_store = []
        self.pos_r_store = []
        self.d_rpm_l_store = []
        self.d_rpm_r_store = []
        self.d_pos_l_store = []
        self.d_pos_r_store = []

        self.time_stamp = []

        self.Kp = 2.5
        self.Ki = 0.0
        self.Kd = 0.3

        self.prev_error = 0.0
        self.integral = 0.0
        self.setpoint_yaw = None

        self.max_speed = 30

        self.rpm_cmd_left = 0
        self.rpm_cmd_right = 0

        self.get_logger().info('---- Motor node started ----')

    def read_csv_file(self, filename):
        pos_data = []
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                pos_data.append((int(row['Pos_Left']), int(row['Pos_Right'])))
        return pos_data
    
    def difference_between_angles(self, first_angle, second_angle):
        difference = (second_angle - first_angle + 180) % 360 -180
        return difference
    
    def distance_pos(self, pos_l, pos_r):
        if self.prev_pos_l is not None:
            d_theta_L = self.difference_between_angles(self.prev_pos_l, pos_l)
            self.dist_left_pos += (pi * 2 * self.wheel_radius * (d_theta_L / 360))
            self.prev_pos_l = pos_l
        else:
            self.prev_pos_l = pos_l
        if self.prev_pos_r is not None:
            d_theta_R = self.difference_between_angles(self.prev_pos_r, pos_r)
            self.dist_right_pos += (pi * 2 * self.wheel_radius * (d_theta_R / 360))
            self.prev_pos_r = pos_r
        else:
            self.prev_pos_r = pos_r

    def get_dist_motor(self, left_wheel_rpm, right_wheel_rpm, delta_t):
        d_left_rpm = ((left_wheel_rpm/60) * 2 * pi * self.wheel_radius) * delta_t # meter
        d_right_rpm = ((right_wheel_rpm/60) * 2 * pi * self.wheel_radius) * delta_t # meter
        
        self.d_left_rpm += d_left_rpm
        self.d_right_rpm += d_right_rpm

    def send_rpm_parallel(self, id, rpm):
        if id == 1:
            self.right_drive.send_rpm(_id=1, rpm=rpm)
        elif id == 2:
            self.left_drive.send_rpm(_id=2, rpm=rpm)

    def publish_values(self):
        now = self.get_clock().now()
        time_elapsed = now - self.then
        self.then = now
        time_elapsed = time_elapsed.nanoseconds / 1e9

        rpm_L, cur_L, pos_L = self.left_drive.get_motor_feedback(_id = 2)
        rpm_R, cur_R, pos_R = self.right_drive.get_motor_feedback(_id = 1)

        self.get_dist_motor(rpm_L, rpm_R, time_elapsed)
        self.distance_pos(pos_L, pos_R)

        self.rpm_l_store.append(rpm_L)
        self.rpm_r_store.append(rpm_R)

        self.pos_l_store.append(rpm_L)
        self.pos_r_store.append(rpm_R)

        self.d_rpm_l_store.append(self.d_left_rpm)
        self.d_rpm_r_store.append(self.d_right_rpm)
        self.d_pos_l_store.append(self.dist_left_pos)
        self.d_pos_r_store.append(self.dist_right_pos)

        self.time_stamp.append(time_elapsed)

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
        # self.idx += 1
        # print(pos_L)

    def get_wheel_command(self, msg):
        self.rpm_cmd_left = msg.cmd_value[0]
        self.rpm_cmd_right = msg.cmd_value[1]
        self.get_logger().info(f"RPM command for wheel: {msg.cmd_value}")
        # self.left_drive.send_rpm(_id=2, rpm=self.rpm_cmd_left)
        # self.right_drive.send_rpm(_id=1, rpm=self.rpm_cmd_right)
    
    def straight(self,):
        if -(self.rpm_cmd_left) == self.rpm_cmd_right and self.rpm_cmd_right != 0 and self.rpm_cmd_left != 0:
            if self.setpoint_yaw == None :
                self.setpoint_yaw = self.yaw
                print(self.yaw, self.setpoint_yaw)
            new_left, new_right = self.pid(self.rpm_cmd_left, desired_yaw=self.setpoint_yaw)
            # print(new_left, new_right)
            new_left = max(-self.max_speed, min(new_left, self.max_speed))
            new_right = max(-self.max_speed, min(new_right, self.max_speed))
            # self.left_drive.send_rpm(_id=2, rpm=-new_left)
            # self.right_drive.send_rpm(_id=1, rpm=new_right)
            p1 = Process(target=self.send_rpm_parallel, args=(2, -new_left))
            p2 = Process(target=self.send_rpm_parallel, args=(1, new_right))
            p1.start()
            p2.start()
            p1.join()
            p2.join()
        else :
            self.setpoint_yaw = None
            # self.left_drive.send_rpm(_id=2, rpm=self.rpm_cmd_left)
            # self.right_drive.send_rpm(_id=1, rpm=self.rpm_cmd_right)
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
        # print(self.setpoint_yaw, output, error, base_rpm)
        self.prev_error = error
        return int((base_rpm + output)), int((base_rpm + output))

def main():
    rclpy.init()
    motor_publisher = MotorNode()
    rclpy.spin(motor_publisher)
    motor_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
