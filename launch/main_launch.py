import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    package_name = 'puzzlebot'
    urdf_file_name = 'puzzlebot.urdf'
    urdf_path = os.path.join(
        get_package_share_directory('puzzlebot'),
        'urdf',
        urdf_file_name)
    
    rviz_config_file = os.path.join(
        get_package_share_directory(package_name), 
        'rviz', 
        'odometry_puzzlebot_rviz.rviz')

    with open(urdf_path, 'r') as urdf_file:
        robot_desc = urdf_file.read()

    # Argumentos de lanzamiento
    use_sim_time = DeclareLaunchArgument(
        'use_sim_time', 
        default_value='false', 
        description='Use sim time if true'
    )
    
    algorithm_arg = DeclareLaunchArgument(
        'algorithm',
        default_value='bug0',  # Valor por defecto
        description='Navigation algorithm to use: "bug0" or "bug2"',
        choices=['bug0', 'bug2']  # Valores permitidos
    )

    # Nodos comunes
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
            {'robot_description': robot_desc}
        ],
        arguments=[urdf_path],
    )
    """
    bringup_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("puzzlebot_gazebo"),
                "launch",
                "bringup_simulation_simple_launch.py"
            ])
        )
    )
    """
    localisation_node = Node(
        package='puzzlebot',
        executable='localisation',
        name='localisation',
        output='screen',
    )
    
    kinematic_model_node = Node(
        package='puzzlebot',
        executable='puzzlebot_kinematic_model',
        name='puzzlebot_kinematic_model',
        output='screen',
    )

    joint_state_publisher = Node(
        package='puzzlebot',
        executable='joint_state_pub',
        name='joint_state_pub',
        parameters=[{'x': 1.0, 'y': 0.0, 'z': 0.0}],
        output='screen'
    )
    """
            # Nodo que convierte /camera/compressed → /camera/image_raw
    camera_converter =  Node(
        package='image_transport',
        executable='republish',
        name='image_republish',
        arguments=['compressed', 'raw'],
        remappings=[
            ('in/compressed', '/camera/compressed'),
            ('out', '/camera/image_raw')
        ],
        output='screen',
        )
    """
    """ Un comment to when using puzzy bot in real life
    camera = Node(
        package='ros_deep_learning',
        executable='video_source',
        name='video_source',
        parameters=[
            {"resource": "csi://0"},
            {"width": 320},
            {"height": 240},
            {"codec": "unknown"},
            {"loop": 0},
            {"latency": 2000}
        ],
        output='screen'
    )
    """

    """ Un comment when using puzzy bot in real life
    camera_info = Node(
        package='camera_info_publisher',
        executable='camera_info_publisher',
        name='camera_info_publisher',
        parameters=[
            {"camera_calibration_file": "file:///home/puzzlebot/.ros/jetson_cam.yaml"},
            {"frame_id": "camera"}  # Debe coincidir con el frame_id de la imagen
        ],
        remappings=[
            ('/camera_info', '/video_source/camera_info')  # <--- Asegúrate que coincida
        ],
        output='screen'
    )
    """
    aruco_detctor = Node(
        package='aruco_opencv',
        executable='aruco_tracker_autostart',
        name='aruco_tracker',
        parameters=[
            {'cam_base_topic': '/video_source/image_raw'},
            {'marker_size': 0.14},
            {'marker_dict': '4X4_50'},
        ],
        output='screen',
    )

    rqt_view = Node(
        package='rqt_image_view',
        executable='rqt_image_view',
        name='rqt_image_view',
        arguments=['/camera/compressed'],
        output='screen'
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

    rqt_tf_tree = Node(
        package='rqt_tf_tree',
        executable='rqt_tf_tree',
        name='rqt_tf_tree',
        output='screen'
    )

    # Nodos condicionales según el algoritmo seleccionado
    navigation_node = Node(
        package='puzzlebot',
        executable=LaunchConfiguration('algorithm'),  # Usa el argumento como nombre del ejecutable
        name=LaunchConfiguration('algorithm'),       # Usa el mismo nombre para el nodo
        output='screen'
    )
    

    return LaunchDescription([
        use_sim_time,
        algorithm_arg,
        #bringup_launch,
        localisation_node,
        navigation_node,
        #camera_info,
        #camera_converter,
        aruco_detctor,
        rqt_view  # Nodo de navegación condicional
        #rqt_graph,
        #rqt_tf_tree
    ])