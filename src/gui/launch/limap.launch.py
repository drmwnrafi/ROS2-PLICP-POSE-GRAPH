import socket
import fcntl
import struct
import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    # Declare the launch argument
    ld.add_action(DeclareLaunchArgument(
        'online',
        default_value='false',
        description='Specifies whether to use online mode or not'
    ))

    # Get IP addresses
    ip_addresses = get_ip_addresses()
    address = get_local_ip(ip_addresses)

    print("address : ", address)
    # Add rosboard_node with parameters
    ld.add_action(Node(
        package='rosboard',
        executable='rosboard_node',
        name='rosboard_node',
        output='screen',
        parameters=[{'port': 8888, 'address': address}]
    ))

    # Add gui_control with parameters
    ld.add_action(Node(
        package='gui',
        executable='gui_control',
        name='gui_control',
        output='screen',
        parameters=[{'port': 7860, 'address': address}]
    ))

    # Add diff_drive_model
    # ld.add_action(Node(
    #     package='diff_drive',
    #     executable='diff_drive_model',
    #     name='diff_drive_model',
    #     output='screen',
    # ))

    # Link 'base_link' to 'base_footprint'
    ld.add_action(Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_transform_publisher_base_footprint',
        output='screen',
        arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'base_footprint']
    ))

    # Link 'base_footprint' to 'laser_link'
    ld.add_action(Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_transform_publisher_laser_link',
        output='screen',
        arguments=['0', '0', '0', '0', '0', '0', 'base_footprint', 'laser_link']
    ))

    return ld

def get_ip_addresses():
    ip_addresses = {}
    try:
        # Get all network interfaces
        interfaces = socket.if_nameindex()
        for iface in interfaces:
            ifname = iface[1]
            try:
                # Get the IP address of the interface
                ip = socket.inet_ntoa(fcntl.ioctl(
                    socket.socket(socket.AF_INET, socket.SOCK_DGRAM),
                    0x8915,  # SIOCGIFADDR
                    struct.pack('256s', bytes(ifname[:15], 'utf-8'))
                )[20:24])
                ip_addresses[ifname] = ip
            except IOError:
                pass  # Ignore interfaces that don't have an IP address
    except Exception as e:
        print("Error:", e)
    return ip_addresses

def get_local_ip(ip_addresses):
    if 'wlp1s0' in ip_addresses:
        return ip_addresses['wlp1s0']
    else:
        # If not, return '127.0.0.1'
        return '127.0.0.1'
