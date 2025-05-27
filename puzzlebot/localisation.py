import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32
from tf2_ros import Buffer, TransformListener, TransformException
from tf2_ros import TransformBroadcaster
from rclpy import qos
import numpy as np
import transforms3d

class Localisation(Node):
    def __init__(self):
        super().__init__('localisation')

        self.wr_sub = self.create_subscription(Float32, 'VelocityEncR', self.wr_callback, qos.qos_profile_sensor_data)
        self.wl_sub = self.create_subscription(Float32, 'VelocityEncL', self.wl_callback, qos.qos_profile_sensor_data)

        self.odom_pub = self.create_publisher(Odometry, 'odom', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        self.r = 0.05
        self.L = 0.19

        self.x = 0.2
        self.y = 0.2
        self.theta = 0.0
        self.wr = 0.0
        self.wl = 0.0

        self.P = np.diag([0.0, 0.0, 0.0])
        self.A = 8.85e-5
        self.B = -4.6e-6
        self.C = 6.08e-5

        self.prev_time = self.get_clock().now().nanoseconds

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.marker_frame = 'marker_0'
        self.world_frame = 'odom'

        self.create_timer(0.01, self.timer_callback)
        self.get_logger().info("Localisation node started")

    def timer_callback(self):
        current_time = self.get_clock().now().nanoseconds
        dt = (current_time - self.prev_time) * 1e-9

        v = self.r * (self.wr + self.wl) / 2.0
        w = self.r * (self.wr - self.wl) / self.L

        self.update_pose(v, w, dt)
        self.update_covariance(v, w, dt)

        try:
            now = rclpy.time.Time()
            trans = self.tf_buffer.lookup_transform(self.world_frame, self.marker_frame, now)

            z_x = trans.transform.translation.x
            z_y = trans.transform.translation.y
            z = np.array([[z_x], [z_y]])

            H = np.array([[1, 0, 0], [0, 1, 0]])
            R = np.diag([0.05**2, 0.05**2])

            x_est = np.array([[self.x], [self.y], [self.theta]])
            y_tilde = z - H @ x_est
            S = H @ self.P @ H.T + R
            K = self.P @ H.T @ np.linalg.inv(S)
            x_corr = x_est + K @ y_tilde
            self.x, self.y, self.theta = x_corr.flatten()
            self.P = (np.eye(3) - K @ H) @ self.P

            self.get_logger().info("EKF correction applied")

        except TransformException:
            pass

        self.prev_time = current_time
        self.publish_odometry()

    def update_covariance(self, v, w, dt):
        J_h = np.array([
            [1, 0, -v * dt * np.sin(self.theta)],
            [0, 1,  v * dt * np.cos(self.theta)],
            [0, 0, 1]
        ])
        Q = np.array([
            [self.A, self.B, self.B],
            [self.B, self.A, self.B],
            [self.B, self.B, self.C]
        ])
        self.P = J_h @ self.P @ J_h.T + Q

    def wr_callback(self, msg):
        self.wr = msg.data

    def wl_callback(self, msg):
        self.wl = msg.data

    def update_pose(self, v, w, dt):
        self.x += v * np.cos(self.theta) * dt
        self.y += v * np.sin(self.theta) * dt
        self.theta += w * dt
        self.theta = np.arctan2(np.sin(self.theta), np.cos(self.theta))

    def publish_odometry(self):
        odom_msg = Odometry()
        odom_msg.header.stamp = self.get_clock().now().to_msg()
        odom_msg.header.frame_id = "odom"
        odom_msg.child_frame_id = "base_link"

        odom_msg.pose.pose.position.x = self.x
        odom_msg.pose.pose.position.y = self.y
        odom_msg.pose.pose.position.z = 0.05

        q = transforms3d.euler.euler2quat(0, 0, self.theta)
        odom_msg.pose.pose.orientation.x = q[1]
        odom_msg.pose.pose.orientation.y = q[2]
        odom_msg.pose.pose.orientation.z = q[3]
        odom_msg.pose.pose.orientation.w = q[0]

        odom_msg.pose.covariance = [0.0]*36
        odom_msg.pose.covariance[0] = self.P[0,0]
        odom_msg.pose.covariance[7] = self.P[1,1]
        odom_msg.pose.covariance[35] = self.P[2,2]
        odom_msg.pose.covariance[1] = self.P[0,1]
        odom_msg.pose.covariance[6] = self.P[1,0]
        odom_msg.pose.covariance[5] = self.P[0,2]
        odom_msg.pose.covariance[30] = self.P[2,0]
        odom_msg.pose.covariance[11] = self.P[1,2]
        odom_msg.pose.covariance[31] = self.P[2,1]

        self.odom_pub.publish(odom_msg)

def main(args=None):
    rclpy.init(args=args)
    node = Localisation()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()
