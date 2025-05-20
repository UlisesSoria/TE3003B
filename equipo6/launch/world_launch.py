from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, SetEnvironmentVariable, 
                            IncludeLaunchDescription, SetLaunchConfiguration)
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration, TextSubstitution, Command, PythonExpression
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource

#IMPORTS REQUIRED TO SET THE PACKAGE ADDRESS (DIRECTORIES)
import os

#IMPORTS REQUIRED FOR Launching Nodes
from launch_ros.parameter_descriptions import ParameterValue

#IMPORTS REQUIRED FOR EVENTS AND ACTIONS
from launch.conditions import IfCondition, UnlessCondition

def generate_launch_description():

    # World and robot file names
    world_file = 'act3_4.world'
    robot = 'puzzlebot_jetson_lidar_ed'
    rviz_file = 'navigation rviz.rviz'
    rviz_config_file = os.path.join(get_package_share_directory('equipo6'), 'rviz', rviz_file)
    mode = LaunchConfiguration('mode')

    # Robot's initial position
    pos_x = '0.2'
    pos_y = '0.2'
    pos_th = '1.6'

    # Simulation time and pause settings
    sim_time = 'true'
    pause_gazebo = 'false'

    # Frame names
    camera_frame = 'camera_link_optical'
    lidar_frame = 'laser'
    tof_frame = 'tof_link'

    # Gazebo verbosity level
    gazebo_verbosity = 4

    # Get package directories
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    models = get_package_share_directory('puzzlebot_description')
    gazebo_resources = get_package_share_directory('equipo6')

    # Paths
    robot_path = os.path.join(models, 'urdf', 'mcr2_robots', f"{robot}.xacro")
    world_path = os.path.join(gazebo_resources, 'worlds', world_file)
    gazebo_models_path = os.path.join(gazebo_resources, 'models')
    gazebo_plugins_path = os.path.join(gazebo_resources,'plugins')
    gazebo_media_path = os.path.join(gazebo_models_path,'models', 'media', 'materials')
    param_nav2 = '/home/ulisess/TE3003B/modulo_3/ActFinal/puzzlebot.yaml'
    map_path = '/home/ulisess/TE3003B/modulo_3/ActFinal/my_map_equipo6.yaml'
    nav2_dir = get_package_share_directory('nav2_bringup')
    default_ros_gz_bridge_config_file_path = os.path.join(gazebo_resources, 'config', f"{robot}.yaml")

    # Launch arguments
    declare_x_arg = DeclareLaunchArgument('x', default_value=pos_x, description='X position of the robot')
    declare_y_arg = DeclareLaunchArgument('y', default_value=pos_y, description='Y position of the robot')
    declare_th_arg = DeclareLaunchArgument('yaw', default_value=pos_th, description='angle of the robot')
    declare_sim_time_arg = DeclareLaunchArgument('use_sim_time', default_value=sim_time, description='Use simulated time')
    declare_pause_arg = DeclareLaunchArgument('pause', default_value=pause_gazebo, description='Start Gazebo paused')
    declare_camera_frame_arg = DeclareLaunchArgument('camera_frame', default_value=camera_frame, description='Camera frame')
    declare_tof_frame_arg = DeclareLaunchArgument('tof_frame', default_value=tof_frame, description='TOF sensor frame')
    declare_lidar_frame_arg = DeclareLaunchArgument('lidar_frame', default_value=lidar_frame, description='Lidar sensor frame')

    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    yaw = LaunchConfiguration('yaw')
    use_sim_time = LaunchConfiguration('use_sim_time')
    pause = LaunchConfiguration('pause')
    camera_frame_name = LaunchConfiguration('camera_frame')
    tof_frame_name = LaunchConfiguration('tof_frame')
    lidar_frame_name = LaunchConfiguration('lidar_frame')

    # Set Gazebo environment variables
    set_gazebo_resources = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=f"{gazebo_models_path}:{gazebo_media_path}"
    )

    set_gazebo_plugins = SetEnvironmentVariable(
        name='GZ_SIM_SYSTEM_PLUGIN_PATH',
        value=f"{gazebo_plugins_path}"
    )

    # Robot description using xacro
    robot_description = Command([
        'xacro ', str(robot_path),
        ' camera_frame:=', camera_frame_name,
        ' tof_frame:=', tof_frame_name,
        ' lidar_frame:=', lidar_frame_name,
    ])

    gz_launch_path = PathJoinSubstitution([pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py'])

    start_gazebo_server_run = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_launch_path),
        launch_arguments={
            'gz_args':  ['-r' f'-v {gazebo_verbosity} ', world_path],
            'on_exit_shutdown': 'true',
        }.items(),
        condition=UnlessCondition(pause)
    )

    start_gazebo_server_paused = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_launch_path),
        launch_arguments={
            'gz_args':  [f'-v {gazebo_verbosity} ', world_path],
            'on_exit_shutdown': 'true',
            'pause': 'true',
        }.items(),
        condition=IfCondition(pause)
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{
            "robot_description": ParameterValue(robot_description, value_type=str),
            "use_sim_time": use_sim_time,
        }],
    )

    odometry_node = Node(
        package="equipo6",
        executable="odometry_publisher",
        name="odometry_publisher",
        output="screen",
    )

    joint_state_publisher_node = Node(
        package="equipo6",
        executable="joint_state_pub",
        name="joint_state_pub",
        output="screen",
        parameters=[{
            "x": x,
            "y": y,
            "z": '0.0',
            "frame": 'odom',
        }],
    )

    localisation_node = Node(
        package="equipo6",
        executable="localisation",
        name="localisation",
        output="screen"
    )

    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-name", "puzzlebot",
            "-topic", "robot_description",
            "-x", x, "-y", y, "-Y", yaw,
        ],
        output="screen",
    )

    start_gazebo_ros_bridge_cmd = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': default_ros_gz_bridge_config_file_path,
        }],
        output='screen')

    start_gazebo_ros_image_bridge_cmd = None
    if robot != "puzzlebot_hacker_ed":
        start_gazebo_ros_image_bridge_cmd = Node(
            package='ros_gz_image',
            executable='image_bridge',
            arguments=[PathJoinSubstitution([TextSubstitution(text='camera')])]
        )


    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file],
        parameters=[{
            'use_sim_time': use_sim_time,
        }],
    )

    # === Nav2 Bringup ===
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([nav2_dir, 'launch', 'bringup_launch.py'])
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'autostart': 'true',
            'params_file': param_nav2,
            'map': map_path,
        }.items()
    )


    # Launch description
    l_d = [
        declare_x_arg, declare_y_arg, declare_th_arg, declare_sim_time_arg, declare_pause_arg, 
        declare_camera_frame_arg, declare_tof_frame_arg, declare_lidar_frame_arg,
        robot_state_publisher_node, odometry_node, nav2_launch,localisation_node, rviz_node,
    ]

    if start_gazebo_ros_image_bridge_cmd:
        l_d.append(start_gazebo_ros_image_bridge_cmd)

    return LaunchDescription(l_d)