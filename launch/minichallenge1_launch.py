import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

def generate_launch_description():
    package_name = 'puzzlebot'
    urdf_file_name = 'puzzlebot.urdf'
    urdf_file_name2 = 'puzzlebot2.urdf'
    urdf_path =os.path.join(
        get_package_share_directory('puzzlebot'),
        'urdf',
        urdf_file_name)
    urdf_path2 =os.path.join(
        get_package_share_directory('puzzlebot'),
        'urdf',
        urdf_file_name2)
    
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
                            emulate_tty=True,
                            output='screen',
                            parameters=[
                                        {'use_sim_time': LaunchConfiguration('use_sim_time')},
                                        {'robot_description': robot_desc}],
                            arguments=[urdf_path],
                            namespace='robot1')
    
    localisation_node = Node(
        package='puzzlebot',
        executable='localisation',
        name='localisation',
        emulate_tty=True,
        output='screen',
        namespace='robot1'
    )
    kinematic_model_node = Node(
        package='puzzlebot',
        executable='puzzlebot_kinematic_model',
        name='puzzlebot_kinematic_model',
        emulate_tty=True,
        output='screen',
        namespace='robot1'
    )


    joint_state_publisher = Node(
        package='puzzlebot',
        executable='joint_state_pub',
        name='joint_state_pub',
        emulate_tty=True,
        output='screen',
        namespace='robot1'
    )

    dynamic_tf_node = Node(
        package='puzzlebot',
        executable='minichallenge1',
        name='minichallenge1',
        parameters=[{'x': 1.0, 'y': 0.0, 'z': 0.0}],
        emulate_tty=True,
        output='screen',
        namespace='robot1'
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen'
    )

    rqt_graph = Node(
        package='rqt_graph',
        executable='rqt_graph',
        name='rqt_graph',
        output='screen'
    )

    robot_state_publisher2 = Node(
                            package='robot_state_publisher',
                            executable='robot_state_publisher',
                            name='robot_state_publisher',
                            emulate_tty=True,
                            output='screen',
                            namespace='robot2',
                            parameters=[
                                        {'use_sim_time': LaunchConfiguration('use_sim_time')},
                                        {'robot_description': robot_desc}],
                            arguments=[urdf_path2])
    
    localisation_node2 = Node(
        package='puzzlebot',
        executable='localisation',
        name='localisation',
        emulate_tty=True,
        output='screen',
        namespace='robot2'
    )
    kinematic_model_node2 = Node(
        package='puzzlebot',
        executable='puzzlebot_kinematic_model',
        name='puzzlebot_kinematic_model',
        emulate_tty=True,
        output='screen',
        namespace='robot2'
    )


    joint_state_publisher2 = Node(
        package='puzzlebot',
        executable='joint_state_pub',
        name='joint_state_pub',
        emulate_tty=True,
        output='screen',
        namespace='robot2'
    )

    dynamic_tf_node2 = Node(
        package='puzzlebot',
        executable='minichallenge1',
        name='minichallenge1',
        parameters=[{'x': 2.0, 'y': 0.0, 'z': 0.0}],
        emulate_tty=True,
        output='screen',
        namespace='robot2'
    )


    return LaunchDescription([
        use_sim_time,
        robot_state_publisher,
        localisation_node,
        kinematic_model_node,
        joint_state_publisher,
        dynamic_tf_node,
        robot_state_publisher2,
        localisation_node2,
        kinematic_model_node2,
        joint_state_publisher2,
        dynamic_tf_node2,
        rviz,
        rqt_graph,

    ])