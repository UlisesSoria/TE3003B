import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Point
import numpy as np

class EKFNode(Node):
    def __init__(self):
        super().__init__('ekf_localization_node')

        # Subscriptions
        self.create_subscription(Twist, 'cmd_vel', self.cmd_vel_callback, 10)
        self.create_subscription(Point, 'measured_pos', self.measurement_callback, 10)

        # Time step (10 Hz)
        self.dt = 0.1
        self.timer = self.create_timer(self.dt, self.ekf_predict)

        # Initial estimated state: [x, y, theta]
        self.x_est = np.array([[0.0], [0.0], [0.0]])

        # Initial covariance matrix
        self.P = np.eye(3) * 0.01

        # Process noise covariance matrix Q
        self.Q = np.array([
            [0.0025, 0.0,   0.0],
            [0.0,    0.0025, 0.0],
            [0.0,    0.0,   0.001]
        ])

        # Measurement noise covariance matrix R (assume 5cm measurement noise)
        self.R = np.diag([0.05**2, 0.05**2])

        # Observation matrix H: maps state to measurement space
        self.H = np.array([
            [1, 0, 0],
            [0, 1, 0]
        ])

        # Latest control inputs
        self.v = 0.0
        self.w = 0.0

        # Latest received measurement (x, y)
        self.z = None

    def cmd_vel_callback(self, msg):
        # Save the latest control input
        self.v = msg.linear.x
        self.w = msg.angular.z

    def measurement_callback(self, msg):
        # Save the latest position measurement
        self.z = np.array([[msg.x], [msg.y]])

    def ekf_predict(self):
        # Prediction step of the EKF

        theta = self.x_est[2, 0]

        # Jacobian of the motion model w.r.t. the state
        Fx = np.array([
            [1, 0, -self.v * np.sin(theta) * self.dt],
            [0, 1,  self.v * np.cos(theta) * self.dt],
            [0, 0, 1]
        ])

        # Control input model
        Bu = np.array([
            [np.cos(theta) * self.dt],
            [np.sin(theta) * self.dt],
            [self.dt]
        ])

        # Control input vector
        u = np.array([[self.v], [self.w]])

        # State prediction
        self.x_est = self.x_est + Bu @ u

        # Covariance prediction
        self.P = Fx @ self.P @ Fx.T + self.Q

        # If a measurement is available, perform update
        if self.z is not None:
            self.ekf_update(self.z)
            self.z = None  # Clear after update

        # Log current estimated pose
        self.get_logger().info(
            f'Estimated position: x={self.x_est[0,0]:.2f}, y={self.x_est[1,0]:.2f}, θ={np.rad2deg(self.x_est[2,0]):.2f}°')

    def ekf_update(self, z):
        # Update step of the EKF

        # Predicted measurement
        z_pred = self.H @ self.x_est

        # Innovation (residual)
        y = z - z_pred

        # Innovation covariance
        S = self.H @ self.P @ self.H.T + self.R

        # Kalman gain
        K = self.P @ self.H.T @ np.linalg.inv(S)

        # State update
        self.x_est = self.x_est + K @ y

        # Covariance update
        self.P = (np.eye(3) - K @ self.H) @ self.P

def main(args=None):
    rclpy.init(args=args)
    node = EKFNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
