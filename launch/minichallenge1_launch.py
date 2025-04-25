import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

def generate_launch_description():
    package_name = 'puzzlebot'
    urdf_file_name = 'puzzlebot.urdf'
    urdf_path =os.path.join(
        get_package_share_directory('puzzlebot'),
        'urdf',
        urdf_file_name)
    #urdf_file_path = os.path.join(get_package_share_directory(package_name), 'urdf', 'puzzlebot.urdf')
    rviz_config_file = os.path.join(get_package_share_directory(package_name), 'rviz', 'puzzlebot.rviz')


    with open(urdf_path, 'r') as urdf_file:
        robot_desc = urdf_file.read()

    use_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='false', description='Use sim time if true'
    )

    robot_state_publisher = Node(
                            package='robot_state_publisher',
                            executable='robot_state_publisher',
                            name='robot_state_publisher',
                            output='screen',
                            parameters=[
                                        {'use_sim_time': LaunchConfiguration('use_sim_time')},
                                        {'robot_description': robot_desc}],
                            arguments=[urdf_path])

    joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui'
    )

    dynamic_tf_node = Node(
        package='puzzlebot',
        executable='minichallenge1',
        name='minichallenge1',
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
        dynamic_tf_node,
        rqt_tf_tree,
        rviz,

        
    ])