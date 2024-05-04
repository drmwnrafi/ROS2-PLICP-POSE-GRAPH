import numpy as np
import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid
from tf_transformations import euler_from_quaternion

class OccupancyMap:
    def __init__(self, resolution) -> None:
        self.xy_resolution = resolution
        self.EXTEND_AREA = 2.0
    
    def bresenham(self, start, end):
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1
        is_steep = abs(dy) > abs(dx)
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        swapped = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            swapped = True
        dx = x2 - x1
        dy = y2 - y1
        error = int(dx / 2.0)
        y_step = 1 if y1 < y2 else -1
        y = y1
        points = []
        for x in range(x1, x2 + 1):
            coord = [y, x] if is_steep else (x, y)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += y_step
                error += dx
        if swapped:
            points.reverse()
        points = np.array(points)
        return points
    
    def generate_ray_casting_grid_map(self, x, y):
        '''
        x : all scan in x axis
        y : all scan in y axis
        '''
        min_x = round(min(x) - self.EXTEND_AREA / 2.0)
        min_y = round(min(y) - self.EXTEND_AREA / 2.0)
        max_x = round(max(x) + self.EXTEND_AREA / 2.0)
        max_y = round(max(y) + self.EXTEND_AREA / 2.0)
        xw = int(round((max_x - min_x) / self.xy_resolution))
        yw = int(round((max_y - min_y) / self.xy_resolution))
    
        occupancy_map = np.ones((xw, yw)) / 2
        center_x = int(round(-min_x / self.xy_resolution))
        center_y = int(round(-min_y / self.xy_resolution))
        for (x, y) in zip(x, y):
            ix = int(round((x - min_x) / self.xy_resolution))
            iy = int(round((y - min_y) / self.xy_resolution))
            laser_beams = self.bresenham((center_x, center_y), (ix, iy))
            for laser_beam in laser_beams:
                occupancy_map[laser_beam[0]][laser_beam[1]] = 0.0
            occupancy_map[ix:ix+2, iy:iy+2] = 1.0
        return occupancy_map, min_x, max_x, min_y, max_y, self.xy_resolution

class MapNode(Node):
    def __init__(self):
        super().__init__('occ_map')
        self.get_logger().info('== Map Node Started ==')

        self.map_resolution = self.declare_parameter('~map_resolution', 0.1).value
        self.map_size_x = self.declare_parameter('~map_size_x', 54.0).value
        self.map_size_y = self.declare_parameter('~map_size_y', 54.0).value
        self.update_movement = self.declare_parameter('~update_movement', 0.1).value

        self.map_msg.info.width = int(self.map_size_x / self.map_resolution)
        self.map_msg.info.height = int(self.map_size_y / self.map_resolution)
        
        self.occupancy = OccupancyMap(self.map_resolution)
        self.laser_sub = self.create_subscription(LaserScan, "scan", self.laser_callback, 10)
        self.odom_sub = self.create_subscription(Odometry, "odom", self.odom_callback, 10)
        self.map_pub = self.create_publisher(OccupancyGrid, "map", 10)
        self.pose = (0.0, 0.0, 0.0)
        self._in_x = []
        self._in_y = []

    def odom_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        z = msg.pose.pose.position.z
        
        qx = msg.pose.pose.orientation.x
        qy = msg.pose.pose.orientation.y
        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w
        quaternion = [qx, qy, qz, qw]
        
        (roll, pitch, yaw) = euler_from_quaternion(quaternion)
        self.pose = (x, y, yaw)

    def polar_to_cartesian(self, ranges, angle_increment, min):
        cartesian_x = []
        cartesian_y = []

        for i, r in enumerate(ranges):
            if np.isinf(r) or np.isnan(r):
                continue

            theta = min + (i * angle_increment)
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            
            cartesian_x.append(x)
            cartesian_y.append(y)
        
        return cartesian_x, cartesian_y

    def laser_callback(self, msg):
        self.laser_data = msg.ranges
        print(len(msg.ranges))
        self._in_x, self._in_y = self.polar_to_cartesian(msg.ranges, msg.angle_increment, msg.angle_min)
        self.publish_occupancy()

    def publish_occupancy(self):
        occupancy_map, min_x, max_x, min_y, max_y, xy_resolution =\
            self.occupancy.generate_ray_casting_grid_map(self._in_x, self._in_y)
        map_msg = OccupancyGrid()
        print(len(self._in_x))
        map_msg.header.frame_id = "map"
        map_msg.info.resolution = xy_resolution
        map_msg.info.origin.position.x = float(self.pose[0])
        map_msg.info.origin.position.y = float(self.pose[1])
        map_msg.info.origin.position.z = 0.0
        map_msg.info.origin.orientation.w = float(self.pose[2])
        
        flattened_map = np.array(occupancy_map * 100, dtype=np.int8).flatten()
        map_msg.data = flattened_map.tolist()
        
        self.map_pub.publish(map_msg)
        self.get_logger().info('== Map Published ==')

def main():
    rclpy.init()
    reading_laser = MapNode()                  
    rclpy.spin(reading_laser)
    reading_laser.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()


```
############
```

import numpy as np
import rclpy
import rclpy.duration
import rclpy.logging
from rclpy.node import Node
from nav_msgs.msg import Odometry
import rclpy.time
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid
import tf2_ros as tf
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException

# p(x) = 1 - \frac{1}{1 + e^l(x)}
def l2p(l):
    return 1 - (1/(1+np.exp(l)))

# l(x) = log(\frac{p(x)}{1 - p(x)})
def p2l(p):
    return np.log(p/(1-p))


class GridMapping:
    def __init__(self, map_center_x, map_center_y, map_size_x, map_size_y, map_resolution, laser_min_angle, laser_max_angle, laser_resolution, laser_max_dist, sensor_model_p_occ, sensor_model_p_free, sensor_model_p_prior):
        self.map_center_x = map_center_x          #meter
        self.map_center_y = map_center_y          #meter
        self.map_size_x = map_size_x              #meter
        self.map_size_y = map_size_y              #meter
        self.map_resolution = map_resolution      #meter/cell
        self.laser_min_angle = laser_min_angle    #radian
        self.laser_max_angle = laser_max_angle    #radian
        self.laser_resolution = laser_resolution  #radian
        self.laser_max_dist = laser_max_dist      #meter
        self.sensor_model_l_occ = p2l(sensor_model_p_occ)
        self.sensor_model_l_free = p2l(sensor_model_p_free)
        self.sensor_model_l_prior = p2l(sensor_model_p_prior)

        map_rows = int(map_size_y / map_resolution)
        map_cols = int(map_size_x / map_resolution)
        self.gridmap = self.sensor_model_l_prior * np.ones((map_rows, map_cols))

    def to_xy(self, i, j):
        x = j * self.map_resolution + self.map_center_x
        y = i * self.map_resolution + self.map_center_y
        return x, y

    def to_ij(self, x, y):
        i = (y - self.map_center_y) / self.map_resolution
        j = (x - self.map_center_x) / self.map_resolution
        return i, j

    def is_inside(self, i, j):
        return 0 <= i < self.gridmap.shape[0] and 0 <= j < self.gridmap.shape[1]

    def raycast_update(self, x0, y0, theta, d):
        if np.isinf(d) and np.sign(d) == +1:
            d = self.laser_max_dist
        elif np.isinf(d) or np.isnan(d):
            return

        x1 = x0 + d * np.cos(theta)
        y1 = y0 + d * np.sin(theta)
        i0, j0 = self.to_ij(x0, y0)
        i1, j1 = self.to_ij(x1, y1)
        d_cells = d / self.map_resolution
        ip, jp, is_hit = self.bresenham(i0, j0, i1, j1, d_cells)
        if not np.isnan(d) and d != self.laser_max_dist and self.is_inside(int(ip), int(jp)):
            # Hit!
            self.gridmap[int(ip), int(jp)] += self.sensor_model_l_occ - self.sensor_model_l_prior
        return

    def bresenham(self, i0, j0, i1, j1, d, debug=False):
        dx = np.absolute(j1 - j0)
        dy = -1 * np.absolute(i1 - i0)
        sx = -1 if j0 < j1 else 1
        sy = -1 if i0 < i1 else 1
        jp, ip = j0, i0
        err = dx + dy
        while True:
            if (jp == j1 and ip == i1) or (
                    np.sqrt((jp - j0) ** 2 + (ip - i0) ** 2) >= d) or not self.is_inside(ip, jp):
                return ip, jp, False
            elif self.gridmap[int(ip), int(jp)] == 100:
                return ip, jp, True

            if self.is_inside(ip, jp):
                self.gridmap[int(ip), int(jp)] += self.sensor_model_l_free - self.sensor_model_l_prior

            e2 = 2 * err
            if e2 >= dy:
                err += dy
                jp += sx
            if e2 <= dx:
                err += dx
                ip += sy

    def update(self, x, y, theta, scan):
        for i, z in enumerate(scan):
            self.raycast_update(x, y, (theta + self.laser_min_angle + i * self.laser_resolution), z)
        return self.gridmap


class GridMappingROS(Node):
    def __init__(self):
        super().__init__('RosGridMapping')
        self.is_grid_initialized = False
        self.map_last_publish = self.get_clock().now().to_msg()
        self.prev_robot_x = -99999999
        self.prev_robot_y = -99999999

        self.sensor_model_p_occ = self.declare_parameter('~sensor_model_p_occ', 0.75).value
        self.sensor_model_p_free = self.declare_parameter('~sensor_model_p_free', 0.45).value
        self.sensor_model_p_prior = self.declare_parameter('~sensor_model_p_prior', 0.5).value
        self.robot_frame = self.declare_parameter('~robot_frame', 'base_link').value
        self.map_frame = self.declare_parameter('~map_frame', 'map').value
        self.map_center_x = self.declare_parameter('~map_center_x', -1.0).value
        self.map_center_y = self.declare_parameter('~map_center_y', -1.0).value
        self.map_size_x = self.declare_parameter('~map_size_x', 54.0).value
        self.map_size_y = self.declare_parameter('~map_size_y', 54.0).value
        self.map_resolution = self.declare_parameter('~map_resolution', 0.1).value
        self.map_publish_freq = self.declare_parameter('~map_publish_freq', 1.0).value
        self.update_movement = self.declare_parameter('~update_movement', 0.1).value

        self.map_msg = OccupancyGrid()
        self.map_msg.header.frame_id = self.map_frame
        self.map_msg.info.resolution = self.map_resolution
        self.map_msg.info.width = int(self.map_size_x / self.map_resolution)
        self.map_msg.info.height = int(self.map_size_y / self.map_resolution)
        self.map_msg.info.origin.position.x = 0.0
        self.map_msg.info.origin.position.y = 0.0

        self.laser_sub = self.create_subscription(LaserScan, "scan", self.laserscan_callback, 10)
        self.map_pub = self.create_publisher(OccupancyGrid, "map", 10)
        self.odom_sub = self.create_subscription(Odometry, "odom", self.odom_callback, 10)
        
        self.tf_buff = tf.Buffer()
        self.tf_broadcaster = tf.TransformBroadcaster(self)
        self.tf_listener = tf.TransformListener(self.tf_buff, self)

        self.x = 0
        self.y = 0
        self.z = 0
        self.qx = 0
        self.qy = 0
        self.qz = 0
        self.qw = 0

    def init_gridmapping(self, laser_min_angle, laser_max_angle, laser_resolution, laser_max_dist):
        self.gridmapping = GridMapping(self.map_center_x, self.map_center_y, self.map_size_x, self.map_size_y,
                                        self.map_resolution, laser_min_angle, laser_max_angle, laser_resolution,
                                        laser_max_dist, self.sensor_model_p_occ, self.sensor_model_p_free,
                                        self.sensor_model_p_prior)
        self.is_grid_initialized = True

    def quaternion_to_yaw(self, qx, qy, qz, qw):
        siny_cosp = 2 * (qw * qz + qx * qy)
        cosy_cosp = 1 - 2 * (qy * qy + qz * qz)
        return np.arctan2(siny_cosp, cosy_cosp)

    def publish_occupancygrid(self, gridmap, stamp):
        gridmap_p = l2p(gridmap)
        gridmap_int8 = (gridmap_p * 100).astype(dtype=np.int8)
        self.map_msg.data = gridmap_int8.tolist()
        self.map_msg.header.stamp = stamp
        self.map_pub.publish(self.map_msg)
        self.get_logger().info("Published map!")

    def odom_callback(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        self.z = msg.pose.pose.position.z
        self.qx = msg.pose.pose.orientation.x
        self.qy = msg.pose.pose.orientation.y
        self.qz = msg.pose.pose.orientation.z
        self.qw = msg.pose.pose.orientation.w

    def laserscan_callback(self, data):
        if not self.is_grid_initialized:
            self.init_gridmapping(data.angle_min, data.angle_max, data.angle_increment, data.range_max)

        try:
            x = self.x
            y = self.y
            z = self.z
            qx = self.qx
            qy = self.qy
            qz = self.qz
            qw = self.qw

            theta = self.quaternion_to_yaw(qx, qy, qz, qw)

            if (x - self.prev_robot_x) ** 2 + (y - self.prev_robot_y) ** 2 >= self.update_movement ** 2:
                gridmap = self.gridmapping.update(x, y, theta, data.ranges).flatten()
                self.prev_robot_x = x
                self.prev_robot_y = y
                self.map_last_publish = self.get_clock().now().to_msg()
                self.publish_occupancygrid(gridmap, self.get_clock().now().to_msg())

        except (LookupException, ConnectivityException, ExtrapolationException) as e:
            self.get_logger().error(str(e))


def main(args=None):
    rclpy.init(args=args)
    gm = GridMappingROS()
    rclpy.spin(gm)
    gm.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()



##############
###############
import numpy as np
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry, OccupancyGrid
from sensor_msgs.msg import LaserScan
from tf_transformations import euler_from_quaternion
import tf2_ros as tf
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException

class OccupancyMap:
    def __init__(self, resolution) -> None:
        self.xy_resolution = resolution
        self.EXTEND_AREA = 2.0
    
    def bresenham(self, start, end):
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1
        is_steep = abs(dy) > abs(dx)
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        swapped = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            swapped = True
        dx = x2 - x1
        dy = y2 - y1
        error = int(dx / 2.0)
        y_step = 1 if y1 < y2 else -1
        y = y1
        points = []
        for x in range(x1, x2 + 1):
            coord = [y, x] if is_steep else (x, y)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += y_step
                error += dx
        if swapped:
            points.reverse()
        points = np.array(points)
        return points
    
    def generate_ray_casting_grid_map(self, x, y):
        min_x = round(min(x) - self.EXTEND_AREA / 2.0)
        min_y = round(min(y) - self.EXTEND_AREA / 2.0)
        max_x = round(max(x) + self.EXTEND_AREA / 2.0)
        max_y = round(max(y) + self.EXTEND_AREA / 2.0)
        xw = int(round((max_x - min_x) / self.xy_resolution))
        yw = int(round((max_y - min_y) / self.xy_resolution))
    
        occupancy_map = np.ones((xw, yw)) / 2
        center_x = int(round(-min_x / self.xy_resolution))
        center_y = int(round(-min_y / self.xy_resolution))
        for (x, y) in zip(x, y):
            ix = int(round((x - min_x) / self.xy_resolution))
            iy = int(round((y - min_y) / self.xy_resolution))
            laser_beams = self.bresenham((center_x, center_y), (ix, iy))
            for laser_beam in laser_beams:
                occupancy_map[laser_beam[0]][laser_beam[1]] = 0.0
            occupancy_map[ix:ix+2, iy:iy+2] = 1.0
        return occupancy_map, min_x, max_x, min_y, max_y, self.xy_resolution

class GridMappingROS(Node):
    def __init__(self):
        super().__init__('RosGridMapping')
        self.is_grid_initialized = False
        self.map_last_publish = self.get_clock().now().to_msg()
        self.prev_robot_x = -99999999
        self.prev_robot_y = -99999999

        self.sensor_model_p_occ = self.declare_parameter('~sensor_model_p_occ', 0.75).value
        self.sensor_model_p_free = self.declare_parameter('~sensor_model_p_free', 0.45).value
        self.sensor_model_p_prior = self.declare_parameter('~sensor_model_p_prior', 0.5).value
        self.map_frame = self.declare_parameter('~map_frame', 'map').value
        self.map_center_x = self.declare_parameter('~map_center_x', -1.0).value
        self.map_center_y = self.declare_parameter('~map_center_y', -1.0).value
        self.map_size_x = self.declare_parameter('~map_size_x', 54.0).value
        self.map_size_y = self.declare_parameter('~map_size_y', 54.0).value
        self.map_resolution = self.declare_parameter('~map_resolution', 0.1).value
        self.update_movement = self.declare_parameter('~update_movement', 0.1).value

        self.map_msg = OccupancyGrid()
        self.map_msg.header.frame_id = self.map_frame
        self.map_msg.info.resolution = self.map_resolution
        self.map_msg.info.width = int(self.map_size_x / self.map_resolution)
        self.map_msg.info.height = int(self.map_size_y / self.map_resolution)
        self.map_msg.info.origin.position.x = -0.5 * self.map_msg.info.width
        self.map_msg.info.origin.position.y = -0.5 * self.map_msg.info.origin.position.y
        self.map_msg.header.frame_id = "map"
        self.map_msg.info.resolution = self.map_resolution

        self.laser_sub = self.create_subscription(LaserScan, "scan", self.laserscan_callback, 10)
        self.map_pub = self.create_publisher(OccupancyGrid, "map", 10)
        self.odom_sub = self.create_subscription(Odometry, "odom", self.odom_callback, 10)
        
        self.occupancy = OccupancyMap(self.map_resolution)
        self.tf_buff = tf.Buffer()
        self.tf_broadcaster = tf.TransformBroadcaster(self)
        self.tf_listener = tf.TransformListener(self.tf_buff, self)

        self.x = 0
        self.y = 0
        self.z = 0
        self.qx = 0
        self.qy = 0
        self.qz = 0
        self.qw = 0

    def odom_callback(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        self.z = msg.pose.pose.position.z
        self.qx = msg.pose.pose.orientation.x
        self.qy = msg.pose.pose.orientation.y
        self.qz = msg.pose.pose.orientation.z
        self.qw = msg.pose.pose.orientation.w

    def polar_to_cartesian(self, ranges, angle_increment, min_angle):
        cartesian_x = []
        cartesian_y = []

        for i, r in enumerate(ranges):
            if np.isinf(r) or np.isnan(r):
                continue

            theta = min_angle + (i * angle_increment)
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            
            cartesian_x.append(x)
            cartesian_y.append(y)
        
        return cartesian_x, cartesian_y

    def laserscan_callback(self, data):
        try:
            x = self.x
            y = self.y
            z = self.z
            qx = self.qx
            qy = self.qy
            qz = self.qz
            qw = self.qw

            if (x - self.prev_robot_x) ** 2 + (y - self.prev_robot_y) ** 2 >= self.update_movement ** 2:
                cartesian_x, cartesian_y = self.polar_to_cartesian(data.ranges, data.angle_increment, data.angle_min)
                occupancy_map, min_x, max_x, min_y, max_y, xy_resolution =\
                    self.occupancy.generate_ray_casting_grid_map(cartesian_x, cartesian_y)
                
                flattened_map = np.array(occupancy_map * 100, dtype=np.int8).flatten()
                self.map_msg.data = flattened_map.tolist()
                print(occupancy_map.shape)
                
                self.map_pub.publish(self.map_msg)
                self.get_logger().info('== Map Published ==')

                self.prev_robot_x = x
                self.prev_robot_y = y

        except (LookupException, ConnectivityException, ExtrapolationException) as e:
            self.get_logger().error(str(e))

def main(args=None):
    rclpy.init(args=args)
    gm = GridMappingROS()
    rclpy.spin(gm)
    gm.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()