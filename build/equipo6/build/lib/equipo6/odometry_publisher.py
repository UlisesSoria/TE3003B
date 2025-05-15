
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
import math


class OdometryFromEncoders(Node):
    def __init__(self):
        super().__init__('odometry_from_encoders')

        # Parámetros del robot
        self.declare_parameter('wheel_separation', 0.19)
        self.declare_parameter('wheel_radius', 0.05)
        self.L = self.get_parameter('wheel_separation').get_parameter_value().double_value
        self.r = self.get_parameter('wheel_radius').get_parameter_value().double_value

        # Estado del robot
        self.x = 0.0
        self.y = 0.0
        self.th = 0.0
        self.wr = 0.0
        self.wl = 0.0

        # Publicador de odometría y TF
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        # Subscripciones a los encoders
        self.create_subscription(Float32, '/VelocityEncR', self.wr_callback, 10)
        self.create_subscription(Float32, '/VelocityEncL', self.wl_callback, 10)

        # Timer de actualización (50 Hz)
        self.timer = self.create_timer(0.02, self.update_odometry)
        self.last_time = self.get_clock().now()

    def wr_callback(self, msg):
        self.wr = msg.data

    def wl_callback(self, msg):
        self.wl = msg.data

    def update_odometry(self):
        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds * 1e-9
        self.last_time = current_time

        v = self.r * (self.wr + self.wl) / 2.0
        w = self.r * (self.wr - self.wl) / self.L

        delta_x = v * math.cos(self.th) * dt
        delta_y = v * math.sin(self.th) * dt
        delta_th = w * dt

        self.x += delta_x
        self.y += delta_y
        self.th += delta_th

        # Publicar odometría
        odom_msg = Odometry()
        odom_msg.header.stamp = current_time.to_msg()
        odom_msg.header.frame_id = 'odom'
        odom_msg.child_frame_id = 'base_footprint'

        odom_msg.pose.pose.position.x = self.x
        odom_msg.pose.pose.position.y = self.y
        odom_msg.pose.pose.position.z = 0.0

        q = self.euler_to_quaternion(0, 0, self.th)
        odom_msg.pose.pose.orientation.x = q[0]
        odom_msg.pose.pose.orientation.y = q[1]
        odom_msg.pose.pose.orientation.z = q[2]
        odom_msg.pose.pose.orientation.w = q[3]

        odom_msg.twist.twist.linear.x = v
        odom_msg.twist.twist.angular.z = w

        self.odom_pub.publish(odom_msg)

        # Publicar transformada odom -> base_footprint
        t = TransformStamped()
        t.header.stamp = current_time.to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_footprint'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        self.tf_broadcaster.sendTransform(t)

    def euler_to_quaternion(self, roll, pitch, yaw):
        qx = math.sin(roll / 2) * math.cos(pitch / 2) * math.cos(yaw / 2) - math.cos(roll / 2) * math.sin(pitch / 2) * math.sin(yaw / 2)
        qy = math.cos(roll / 2) * math.sin(pitch / 2) * math.cos(yaw / 2) + math.sin(roll / 2) * math.cos(pitch / 2) * math.sin(yaw / 2)
        qz = math.cos(roll / 2) * math.cos(pitch / 2) * math.sin(yaw / 2) - math.sin(roll / 2) * math.sin(pitch / 2) * math.cos(yaw / 2)
        qw = math.cos(roll / 2) * math.cos(pitch / 2) * math.cos(yaw / 2) + math.sin(roll / 2) * math.sin(pitch / 2) * math.sin(yaw / 2)
        return [qx, qy, qz, qw]


def main(args=None):
    rclpy.init(args=args)
    node = OdometryFromEncoders()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()
