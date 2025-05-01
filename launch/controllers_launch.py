from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    

    controller_node = Node(
        package='puzzlebot',
        executable='controller',
        name='controller',
        output='screen',
        emulate_tty=True,
        parameters=[{'goals': "[[0.0, 1.0], [1.0, 1.0], [-1.0, 0.0], [0.0, 0.0]]"}],
        #namespace='robot1'
    )

    controller_node2 = Node(
        package='puzzlebot',
        executable='controller',
        name='controller',
        output='screen',
        emulate_tty=True,
        parameters=[{'goals': "[[2.0, 0.0], [2.0, 1.0], [1.0, 1.0], [1.0, 0.0]]"}],
        namespace='robot2',
    )

    return LaunchDescription([
        controller_node,
        #controller_node2,
    ])