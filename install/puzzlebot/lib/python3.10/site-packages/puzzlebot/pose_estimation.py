#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, Float32MultiArray, Bool
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
from tf_transformations import quaternion_from_euler
import numpy as np
from numpy.linalg import inv
import tf2_ros

class Localisation(Node):
    def __init__(self):
        super().__init__('localisation')

        # SUBSCRIBERS
        self.create_subscription(Float32, "VelocityEncL", self.wl_cb, 10)
        self.create_subscription(Float32, "VelocityEncR", self.wr_cb, 10)
        self.create_subscription(Float32MultiArray, "aruco_topic", self.aruco_cb, 10)
        self.create_subscription(Bool, "goal_reached", self.goal_cb, 10)

        # PUBLISHERS
        self.odom_pub = self.create_publisher(Odometry, 'odom', 10)
        self.goal_pub = self.create_publisher(Float32MultiArray, 'goalmarker', 10)

        # TF Broadcaster
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)

        # ROBOT CONSTANTS
        self.r = 0.05
        self.L = 0.19
        self.dt = 0.05

        # INITIAL POSITION
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # ARUCO IDENTIFIERS
        self.x_aruco = 0
        self.y_aruco = 0
        self.id_aruco = 0
        self.get_aruco = False

        # VELOCITY VARIABLES
        self.w = 0.0
        self.v = 0.0
        self.wr = 0.0
        self.wl = 0.0
        self.flag = False
        self.first = True

        # EKF VARIABLES
        self.miu = np.array([self.x, self.y, self.theta])
        self.miu_hat = np.array([0, 0, 0])
        self.sigma = np.zeros((3, 3))
        self.sigma_hat = np.zeros((3, 3))
        self.Z = np.zeros((2, 2))
        self.z_hat = np.zeros((2, ))
        self.H = np.zeros((3, 3))
        self.G = np.zeros((2, 3))
        self.gradient_W = np.zeros((3, 2))
        self.Q = np.zeros((3, 3))
        self.R = np.array([[0.02, 0.0], [0.0, 0.004]])
        self.K = np.zeros((3, 2))
        self.covariance = np.zeros((2, 2))

        # GAINS
        self.kl = 0.3
        self.kr = 0.2

        # GOALS
        self.goals = [
            [2.0, 2.0]
        ]
        self.current_goal_index = 0
        self.goal = Float32MultiArray()

        # Timer for main loop
        self.timer = self.create_timer(self.dt, self.main_loop)

    def main_loop(self):
        self.get_logger().info("========================================")
        self.get_logger().info(f"X del robot : {self.x}")
        self.get_logger().info(f"Y del robot : {self.y}")
        self.get_logger().info(f"Theta del robot : {self.theta}\n")

        # Get linear and angular speeds
        self.v = ((self.wr + self.wl) / 2) * self.r
        self.w = ((self.wr - self.wl) / self.L) * self.r

        # Covariance matrix
        self.covariance = np.array([[self.kl * abs(self.wr), 0],
                                    [0, self.kr * abs(self.wl)]])

        # Jacobian matrix
        self.gradient_W = (0.5 * self.r * self.dt) * np.array([
            [np.cos(self.theta), np.cos(self.theta)],
            [np.sin(self.theta), np.sin(self.theta)],
            [2.0 / self.L, -2.0 / self.L]
        ])

        # Noise covariance
        self.Q = self.gradient_W.dot(self.covariance).dot(self.gradient_W.T)

        # Prediction step
        self.prediction()

        # Correction step if aruco detected
        if self.get_aruco:
            self.correction()
            self.get_aruco = False
        else:
            self.propagate()

        # Update odometry
        odom_msg = self.get_odom_stamped()
        self.odom_pub.publish(odom_msg)

        # Send transform
        self.send_transform(odom_msg)

        # Handle goals
        if self.first:
            self.goal.data = self.goals[self.current_goal_index]
            self.current_goal_index += 1
            self.first = False

        if self.flag:
            if self.current_goal_index >= len(self.goals):
                self.get_logger().info("!!!!!!!!All goals reached!!!!!!!!!!!")
                self.flag = False
                return
            self.get_logger().info(f"Target # {self.current_goal_index} at coord: {self.goals[self.current_goal_index]}")
            self.get_logger().info("Wait 5 seconds till next point is published")

            # Wait 5 seconds
            start_time = self.get_clock().now().nanoseconds / 1e9
            end_time = start_time + 5.0
            while (self.get_clock().now().nanoseconds / 1e9) < end_time:
                elapsed_time = self.get_clock().now().nanoseconds / 1e9 - start_time
                percentage = (elapsed_time / 5.0) * 100
                self.get_logger().info(f"Percentage: {percentage:.2f}%")
                rclpy.spin_once(self, timeout_sec=0.1)
            self.get_logger().info("Sending new objective...")
            self.goal.data = self.goals[self.current_goal_index]
            self.current_goal_index += 1
            self.flag = False

        self.goal_pub.publish(self.goal)

    ######################### EXTENDED KALMAN FILTER ########################

    def prediction(self):
        self.miu_hat = np.array([
            self.x + self.dt * self.v * np.cos(self.theta),
            self.y + self.dt * self.v * np.sin(self.theta),
            self.theta + self.dt * self.w
        ])
        self.H = np.array([
            [1, 0, -self.dt * self.v * np.sin(self.theta)],
            [0, 1, self.dt * self.v * np.cos(self.theta)],
            [0, 0, 1]
        ])
        self.sigma_hat = self.H.dot(self.sigma).dot(self.H.T) + self.Q

    def correction(self):
        dx = self.x_aruco - self.x
        dy = self.y_aruco - self.y
        p = dx**2 + dy**2
        if p == 0:
            self.get_logger().warn("Aruco and robot overlap; skipping correction step.")
            return
        self.z_hat = np.array([
            np.sqrt(p),
            np.arctan2(dy, dx) - self.theta
        ])
        self.G = np.array([
            [-dx / np.sqrt(p), -dy / np.sqrt(p), 0],
            [dy / p, -dx / p, -1]
        ])
        self.Z = self.G.dot(self.sigma_hat).dot(self.G.T) + self.R
        self.K = self.sigma_hat.dot(self.G.T).dot(inv(self.Z))
        self.miu = self.miu_hat + self.K.dot((np.array(self.coords_aruco) - self.z_hat))
        self.sigma = (np.eye(3) - self.K.dot(self.G)).dot(self.sigma_hat)

    def propagate(self):
        self.miu = self.miu_hat
        self.x = self.miu[0].item()
        self.y = self.miu[1].item()
        self.theta = self.miu[2].item()
        self.theta = np.arctan2(np.sin(self.theta), np.cos(self.theta))
        self.theta_pred = self.miu_hat[2].item()
        self.theta_pred = np.arctan2(np.sin(self.theta_pred), np.cos(self.theta_pred))
        self.sigma = self.sigma_hat

    ####################### ODOMETRY AND TRANSFORM ###############################
    def get_odom_stamped(self):
        odom_stamped = Odometry()
        odom_stamped.header.frame_id = "odom"
        odom_stamped.child_frame_id = "base_link"
        odom_stamped.header.stamp = self.get_clock().now().to_msg()
        odom_stamped.pose.pose.position.x = float(self.x)
        odom_stamped.pose.pose.position.y = float(self.y)
        odom_stamped.pose.pose.position.z = 0.0

        quat = quaternion_from_euler(0, 0, self.theta)
        odom_stamped.pose.pose.orientation.x = float(quat[0])
        odom_stamped.pose.pose.orientation.y = float(quat[1])
        odom_stamped.pose.pose.orientation.z = float(quat[2])
        odom_stamped.pose.pose.orientation.w = float(quat[3])

        odom_stamped.twist.twist.linear.x = float(self.v)
        odom_stamped.twist.twist.angular.z = float(self.w)

        # Init a 36 elements array
        odom_stamped.pose.covariance = [0.0] * 36
        # Fill the 3D covariance matrix
        odom_stamped.pose.covariance[0] = self.sigma[0][0]
        odom_stamped.pose.covariance[1] = self.sigma[0][1]
        odom_stamped.pose.covariance[5] = self.sigma[0][2]
        odom_stamped.pose.covariance[6] = self.sigma[1][0]
        odom_stamped.pose.covariance[7] = self.sigma[1][1]
        odom_stamped.pose.covariance[11] = self.sigma[1][2]
        odom_stamped.pose.covariance[30] = self.sigma[2][0]
        odom_stamped.pose.covariance[31] = self.sigma[2][1]
        odom_stamped.pose.covariance[35] = self.sigma[2][2]

        return odom_stamped

    def send_transform(self, odom):
        t = TransformStamped()
        t.header.frame_id = "odom"
        t.child_frame_id = "base_link"
        t.header.stamp = self.get_clock().now().to_msg()
        t.transform.translation.x = float(self.x)
        t.transform.translation.y = float(self.y)
        t.transform.translation.z = 0.0

        quat = quaternion_from_euler(0, 0, self.theta)
        t.transform.rotation.x = float(quat[0])
        t.transform.rotation.y = float(quat[1])
        t.transform.rotation.z = float(quat[2])
        t.transform.rotation.w = float(quat[3])

        self.tf_broadcaster.sendTransform(t)

    ###################### CALLBACKS ###########################

    def wl_cb(self, msg):
        self.wl = msg.data

    def wr_cb(self, msg):
        self.wr = msg.data

    def goal_cb(self, msg):
        self.flag = msg.data

    def aruco_cb(self, msg):
        self.id_aruco = int(msg.data[0])
        self.d_aruco = msg.data[1]
        self.theta_aruco = msg.data[2]
        self.coords_aruco = [self.d_aruco, self.theta_aruco]
        self.id_arucos(self.id_aruco)
        self.get_aruco = True

    def id_arucos(self, id):
        x_y = {
            0: [2.5, -0.5], 1: [2.5, 2.5], 3: [-0.5, 2.5],
            4: [-0.5, -0.5]
        }
        if id in x_y:
            self.x_aruco = x_y[id][0]
            self.y_aruco = x_y[id][1]
        else:
            self.get_logger().warn(f"Aruco id {id} not recognized!")

def main(args=None):
    rclpy.init(args=args)
    node = Localisation()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()