from setuptools import find_packages
from setuptools import setup

setup(
    name='wheel_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('wheel_interfaces', 'wheel_interfaces.*')),
)
