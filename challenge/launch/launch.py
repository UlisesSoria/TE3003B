import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

def generate_launch_description():
    package_name = 'challenge'
    urdf_file = os.path.join(get_package_share_directory(package_name), 'urdf', 'puzzlebot.urdf')
    rviz_config_file = os.path.join(get_package_share_directory(package_name), 'rviz', 'puzzlebot.rviz')

    use_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='false', description='Use sim time if true'
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        arguments=[urdf_file]
    )

    joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui'
    )

    static_transform_node = Node(
                                package='tf2_ros',
                                executable='static_transform_publisher',
                                arguments = ['--x', '-0.2', '--y', '0', '--z', '0.0',
                                            '--yaw', '0', '--pitch', '0', '--roll', '0.0',
                                            '--frame-id', 'map', '--child-frame-id', 'odom']
                                )

    static_transform_node_2 = Node(
                                package='tf2_ros',
                                executable='static_transform_publisher',
                                arguments = ['--x', '0', '--y', '0', '--z', '0.05',
                                            '--yaw', '0.0', '--pitch', '0', '--roll', '0.0',
                                            '--frame-id', 'base_footprint', '--child-frame-id', 'base_link']
                                )
    static_transform_node_3 = Node(
                                package='tf2_ros',
                                executable='static_transform_publisher',
                                arguments = ['--x', '-0.095', '--y', '0', '--z', '-0.03',
                                            '--yaw', '0.0', '--pitch', '0', '--roll', '0.0',
                                            '--frame-id', 'base_link', '--child-frame-id', 'caster']
                                )

    dynamic_tf_node = Node(
        package='challenge',
        executable='dynamic_tf_publisher',
        name='dynamic_tf_publisher',
        output='screen'
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen'
    )

    rqt_tf_tree = Node(
        package='rqt_tf_tree',
        executable='rqt_tf_tree',
        name='rqt_tf_tree',
        output='screen'
    )

    return LaunchDescription([
        use_sim_time,
        robot_state_publisher,
        joint_state_publisher_gui,
        static_transform_node,
        static_transform_node_2,
        static_transform_node_3,
        dynamic_tf_node,
        rqt_tf_tree,
        rviz,

        
    ])