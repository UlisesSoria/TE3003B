#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
import numpy as np
import transforms3d

class OdometryFromEncoders(Node):
    def __init__(self):
        super().__init__('kinematic_model')

        # Parámetros del robot
        self.r = 0.05  # radio de rueda [m]
        self.L = 0.19  # separación entre ruedas [m]

        # Estado
        self.wl = 0.0
        self.wr = 0.0
        self.x = 0.2
        self.y = 0.2
        self.theta = 1.6
        self.last_time = self.get_clock().now().nanoseconds * 1e-9

        # Publicadores y suscriptores
        self.odom_pub = self.create_publisher(Odometry, 'odom', 10)
        self.tf_broadcaster = TransformBroadcaster(self)
        self.create_subscription(Float32, 'VelocityEncL', self.wl_callback, 10)
        self.create_subscription(Float32, 'VelocityEncR', self.wr_callback, 10)

        self.timer = self.create_timer(0.02, self.update_odometry)  # 50 Hz

    def wl_callback(self, msg):
        self.wl = msg.data

    def wr_callback(self, msg):
        self.wr = msg.data

    def update_odometry(self):
        now = self.get_clock().now().nanoseconds * 1e-9
        dt = now - self.last_time
        self.last_time = now

        # Cinemática diferencial
        v = self.r * (self.wr + self.wl) / 2.0
        w = self.r * (self.wr - self.wl) / self.L

        # Actualización de pose
        self.x += v * dt * np.cos(self.theta)
        self.y += v * dt * np.sin(self.theta)
        self.theta += w * dt
        self.theta = np.arctan2(np.sin(self.theta), np.cos(self.theta))  # normalización

        # Publicar odometría
        odom_msg = Odometry()
        odom_msg.header.stamp = self.get_clock().now().to_msg()
        odom_msg.header.frame_id = 'odom'
        odom_msg.child_frame_id = 'base_link'
        odom_msg.pose.pose.position.x = self.x
        odom_msg.pose.pose.position.y = self.y
        odom_msg.pose.pose.position.z = 0.0

        quat = transforms3d.euler.euler2quat(0, 0, self.theta)
        odom_msg.pose.pose.orientation.x = quat[1]
        odom_msg.pose.pose.orientation.y = quat[2]
        odom_msg.pose.pose.orientation.z = quat[3]
        odom_msg.pose.pose.orientation.w = quat[0]

        odom_msg.twist.twist.linear.x = v
        odom_msg.twist.twist.angular.z = w

        self.odom_pub.publish(odom_msg)

def main(args=None):
    rclpy.init(args=args)
    node = OdometryFromEncoders()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()