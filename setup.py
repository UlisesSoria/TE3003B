from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'puzzlebot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.[yma]*'))),
        (os.path.join('share', package_name, 'rviz'), glob(os.path.join('rviz', '*.rviz'))),
        (os.path.join('share', package_name, 'meshes'), glob(os.path.join('meshes', '*.stl'))),
        (os.path.join('share', package_name, 'urdf'), glob(os.path.join('urdf', '*.urdf'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ulisess',
    maintainer_email='A01704152@tec.mx',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'minichallenge1 = puzzlebot.minichallenge1:main',
            'puzzlebot_kinematic_model = puzzlebot.puzzlebot_kinematic_model:main',
            'joint_state_pub = puzzlebot.joint_state_pub:main',
            'localisation = puzzlebot.localisation:main',
            'localisationv2 = puzzlebot.localisationv2:main',
            'point_stabilisation_control = puzzlebot.point_stabilisation_control:main',
            'move_forward = puzzlebot.move_forward:main',
            'controller = puzzlebot.controller:main',
        ],
    },
)
