from setuptools import find_packages, setup

package_name = 'icp_graph_slam'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ziczac',
    maintainer_email='drmwnnrafi@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'get_lidar = icp_graph_slam.slam:main',
            'collect_data_mapping = icp_graph_slam.lidar_maping:main'
        ],
    },
)
