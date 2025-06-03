from puzzlebot import maths 
from puzzlebot import puzzlebot_kinematic_model as puzzlebot_kinematics
from puzzlebot import eyes

import rclpy
from rclpy.node import Node
from rclpy import qos
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32
from geometry_msgs.msg import TransformStamped
from tf2_ros import Buffer, TransformListener, TransformBroadcaster
from puzzlebot_aruco_msgs.msg import ArucoObservation
import numpy as np
import json
import transforms3d

class Localisation(Node):
    def __init__(self):
        super().__init__('localisation')

        self.declare_parameter('aruco_observation_noise_matrix', [0.02, 0.001, 0.001, 0.02]) # Noise matrix for ArUco observations
        self.declare_parameter(
    'aruco_poses',
    '{"0": [0.9, 0.6], "1": [1.2, -1.48], "2": [0.3, 0.28], "3": [-1.5, 0.0], "4": [-1.0, -1.48], "5": [-1.2, 1.48]}'
) # ArUco poses in a JSON string format, where the key is the ArUco ID and the value is a list with [x, y] coordinates
        self.declare_parameter('kr', 0.15) # Gaussian noise variance gain for the right wheel speed
        self.declare_parameter('kl', 0.15) # Gaussian noise variance gain for the left wheel speed

        self.wr_sub = self.create_subscription(Float32, 'VelocityEncR', self.wr_callback, qos.qos_profile_sensor_data)
        self.wl_sub = self.create_subscription(Float32, 'VelocityEncL', self.wl_callback, qos.qos_profile_sensor_data)
        self.create_subscription(ArucoObservation, 'aruco_observation', self.aruco_observation_callback, qos.qos_profile_sensor_data)

        self.arucos_observation_noise_matrix = np.array(self.get_parameter('aruco_observation_noise_matrix').get_parameter_value().double_array_value).reshape((2, 2))
        self.aruco_poses = json.loads(self.get_parameter('aruco_poses').get_parameter_value().string_value)
        self.aruco_poses = {int(k): list(map(float, v)) for k, v in self.aruco_poses.items()}
        self.kr = self.get_parameter('kr').get_parameter_value().double_value
        self.kl = self.get_parameter('kl').get_parameter_value().double_value

        self.odom_pub = self.create_publisher(Odometry, 'odom', 10)
        self.pose_pub = self.create_publisher(Odometry, 'puzzlebot_pose', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        self.r = 0.05
        self.L = 0.19

        self.x = -1.2
        self.y = 1.2
        self.theta = 0.0
        self.wr = 0.0
        self.wl = 0.0

        self.prev_time = self.get_clock().now()

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.puzzlebot_kinematic_model = puzzlebot_kinematics.get_puzzlebot_kinematic_model(self.r, self.L) # Kinematic model to go from wheel speeds to robot velocities
        self.wheels_speeds = np.array([0., 0.]) # Wheels speeds in rad/s
        self.puzzlebot_pose = np.array([self.x, self.x, self.theta]) # Puzzlebot pose [x, y, theta] in meters and radians
        self.covariance_matrix = np.zeros((3, 3)) # Covariance matrix for the pose estimation

        self.create_timer(0.05, self.timer_callback)
        self.get_logger().info("Localisation node started")

        self.map_odom_transform = TransformStamped()
        self.map_odom_transform.header.stamp = self.get_clock().now().to_msg()
        self.map_odom_transform.header.frame_id = 'map'
        self.map_odom_transform.child_frame_id = f'odom'
        self.map_odom_transform.transform.translation.x = 0.0
        self.map_odom_transform.transform.translation.y = 0.0
        self.map_odom_transform.transform.translation.z = 0.0
        self.map_odom_transform.transform.rotation.x = 0.0
        self.map_odom_transform.transform.rotation.y = 0.0
        self.map_odom_transform.transform.rotation.z = 0.0
        self.map_odom_transform.transform.rotation.w = 1.0

    def aruco_observation_callback(self, msg):
        # Store the ArUco observation 
        aruco_id = msg.id

        if aruco_id not in self.aruco_poses:
            self.get_logger().warn(f'Received ArUco observation for unknown ID {aruco_id}. Ignoring.')
            return

        aruco_observation = (msg.distance, msg.angle)

        # Get the transform from map to the base_footprint frame
        map_base_footprint_tf = self.tf_buffer.lookup_transform('map', 'base_footprint', rclpy.time.Time(), timeout=rclpy.duration.Duration(seconds=0.25))

        # Store the odometry observation
        delta_x = self.aruco_poses[aruco_id][0] - map_base_footprint_tf.transform.translation.x
        delta_y = self.aruco_poses[aruco_id][1] - map_base_footprint_tf.transform.translation.y
        puzzlebot_theta_from_map = transforms3d.euler.quat2euler([map_base_footprint_tf.transform.rotation.w,
                                                        map_base_footprint_tf.transform.rotation.x,
                                                        map_base_footprint_tf.transform.rotation.y,
                                                        map_base_footprint_tf.transform.rotation.z])[2]
        odometry_observation = eyes.observate_from_deltas(delta_x, delta_y, puzzlebot_theta_from_map)

        # Get the linearized observation matrix
        linearized_observation_matrix = eyes.observate_from_deltas_linearized(delta_x, delta_y)

        # Propagate the covariance matrix into the observation space and add observation noise
        Z = linearized_observation_matrix @ self.covariance_matrix @ linearized_observation_matrix.T + \
            self.arucos_observation_noise_matrix
        
        # Get the Kalman gain
        K = self.covariance_matrix @ linearized_observation_matrix.T @ np.linalg.inv(Z)

        # Get the kalman shift
        kalman_shift = K @ (aruco_observation - odometry_observation)

        # Get the odom to base_footprint transform
        odom_base_footprint_tf = self.tf_buffer.lookup_transform('odom', 'base_footprint', rclpy.time.Time(), timeout=rclpy.duration.Duration(seconds=0.25))
        # Shift the puzzlebot theta using the kalman shift
        puzzlebot_theta_from_map += kalman_shift[2]
        # Convert the puzzlebot theta to quaternion
        q = transforms3d.euler.euler2quat(0.0, 0.0, puzzlebot_theta_from_map)
        # Shift the map to base_footprint transform usin the kalman shift
        map_base_footprint_tf.transform.translation.x += kalman_shift[0]
        map_base_footprint_tf.transform.translation.y += kalman_shift[1]
        map_base_footprint_tf.transform.rotation.x = q[1]
        map_base_footprint_tf.transform.rotation.y = q[2]
        map_base_footprint_tf.transform.rotation.z = q[3]
        map_base_footprint_tf.transform.rotation.w = q[0]

        # Solve for the map to odom transform
        map_odom_transform = maths.transform_to_matrix(map_base_footprint_tf) @ np.linalg.inv(maths.transform_to_matrix(odom_base_footprint_tf))
        # Update the map to odom transform
        self.map_odom_transform.transform.translation.x = map_odom_transform[0, 3]
        self.map_odom_transform.transform.translation.y = map_odom_transform[1, 3]
        self.map_odom_transform.transform.translation.z = map_odom_transform[2, 3]
        q = transforms3d.quaternions.mat2quat(map_odom_transform[:3, :3])
        self.map_odom_transform.transform.rotation.x = q[1]
        self.map_odom_transform.transform.rotation.y = q[2]
        self.map_odom_transform.transform.rotation.z = q[3]
        self.map_odom_transform.transform.rotation.w = q[0]

        # Update the covariance matrix
        self.covariance_matrix = (np.eye(3) - K @ linearized_observation_matrix) @ self.covariance_matrix

    def timer_callback(self):

        speeds = self.puzzlebot_kinematic_model @ self.wheels_speeds
        current_time = self.get_clock().now()
        dt = (current_time - self.prev_time).nanoseconds / 1e-9

        # Get the current linearized puzzlebot model
        linearized_puzzlebot_model = puzzlebot_kinematics.get_linearized_puzzlebot_model_matrix(speeds[0], self.puzzlebot_pose[2], dt)
        # Get the linearized puzzlebot input model
        linearized_puzzlebot_input_model = puzzlebot_kinematics.get_linearized_puzzlebot_input_model_matrix(self.r, self.L, self.puzzlebot_pose[2], dt)

        # Decompose the linear and angular speeds into [vx, vy, w]
        decomposed_speeds = puzzlebot_kinematics.speeds_decomposer(speeds[0], speeds[1], self.puzzlebot_pose[2])

        # Get the 2x2 variance matrix from encoder readings
        wheel_variance = np.array([[self.kr*abs(self.wheels_speeds[0]), 0.0], [0.0, self.kl*abs(self.wheels_speeds[1])]])

        # Update the covariance matrix
        self.covariance_matrix = linearized_puzzlebot_model @ self.covariance_matrix @ linearized_puzzlebot_model.T + \
                                linearized_puzzlebot_input_model @ wheel_variance @ linearized_puzzlebot_input_model.T


        self.update_pose(decomposed_speeds[0], decomposed_speeds[1], dt)

        self.publish_odometry(speeds[0], speeds[1])

        # Update the last time
        self.prev_time = self.get_clock().now()

    def wr_callback(self, msg):
        self.wheels_speeds[0] = msg.data

    def wl_callback(self, msg):
        self.wheels_speeds[1] = msg.data

    def update_pose(self, v, w, dt):
        self.puzzlebot_pose[0] += v * dt
        self.puzzlebot_pose[1] += v * dt
        self.puzzlebot_pose[2] = maths.get_normalized_angle(self.puzzlebot_pose[2] + w * dt)

    def publish_odometry(self, v, w):
        # Odom message
        odom_msg = Odometry()
        odom_msg.header.stamp = self.get_clock().now().to_msg()
        odom_msg.header.frame_id = 'odom'
        odom_msg.child_frame_id = 'base_footprint'
        odom_msg.pose.pose.position.x = self.puzzlebot_pose[0]
        odom_msg.pose.pose.position.y = self.puzzlebot_pose[1]
        odom_msg.pose.pose.position.z = 0.0
        q = transforms3d.euler.euler2quat(0.0, 0.0, self.puzzlebot_pose[2])
        odom_msg.pose.pose.orientation.x = q[1]
        odom_msg.pose.pose.orientation.y = q[2]
        odom_msg.pose.pose.orientation.z = q[3]
        odom_msg.pose.pose.orientation.w = q[0]
        odom_msg.pose.covariance = [0.0] * 36
        odom_msg.pose.covariance[0] = self.covariance_matrix[0, 0]
        odom_msg.pose.covariance[1] = self.covariance_matrix[0, 1]
        odom_msg.pose.covariance[5] = self.covariance_matrix[0, 2]
        odom_msg.pose.covariance[6] = self.covariance_matrix[1, 0]
        odom_msg.pose.covariance[7] = self.covariance_matrix[1, 1]
        odom_msg.pose.covariance[11] = self.covariance_matrix[1, 2]
        odom_msg.pose.covariance[30] = self.covariance_matrix[2, 0]
        odom_msg.pose.covariance[31] = self.covariance_matrix[2, 1]
        odom_msg.pose.covariance[35] = self.covariance_matrix[2, 2]
        odom_msg.twist.twist.linear.x = v
        odom_msg.twist.twist.linear.y = 0.0
        odom_msg.twist.twist.linear.z = 0.0
        odom_msg.twist.twist.angular.x = 0.0
        odom_msg.twist.twist.angular.y = 0.0
        odom_msg.twist.twist.angular.z = w

        # Publish the odometry message
        self.odom_pub.publish(odom_msg)
        self.pose_pub.publish(odom_msg)

        # Update the map odom transform timestamp
        self.map_odom_transform.header.stamp = self.get_clock().now().to_msg()
        # Publish the map odom transform
        self.tf_broadcaster.sendTransform(self.map_odom_transform)  


def main(args=None):
    rclpy.init(args=args)
    node = Localisation()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()
