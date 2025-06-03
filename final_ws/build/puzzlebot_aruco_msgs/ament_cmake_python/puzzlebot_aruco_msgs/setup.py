from setuptools import find_packages
from setuptools import setup

setup(
    name='puzzlebot_aruco_msgs',
    version='0.0.0',
    packages=find_packages(
        include=('puzzlebot_aruco_msgs', 'puzzlebot_aruco_msgs.*')),
)
