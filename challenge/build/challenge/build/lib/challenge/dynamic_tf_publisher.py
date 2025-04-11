import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
import transforms3d


class FramePublisher(Node):

    def __init__(self):
        super().__init__('frame_publisher')

        self.broadcaster = TransformBroadcaster(self)
        self.timer_period = 0.1  # seconds
        self.timer = self.create_timer(self.timer_period, self.timer_cb)

        self.start_time = self.get_clock().now()
        self.omega = 1.0 # Adjusted for Sim aesthetic purposes

    def create_transform(self, parent, child, translation, euler_angles):

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = parent
        t.child_frame_id = child
        t.transform.translation.x = translation[0]
        t.transform.translation.y = translation[1]
        t.transform.translation.z = translation[2]

        q = transforms3d.euler.euler2quat(*euler_angles)  # (roll, pitch, yaw) → (w, x, y, z)
        t.transform.rotation.x = q[1]
        t.transform.rotation.y = q[2]
        t.transform.rotation.z = q[3]
        t.transform.rotation.w = q[0]

        return t

    def timer_cb(self):
        elapsed_time = (self.get_clock().now() - self.start_time).nanoseconds / 1e9
        angle = elapsed_time * self.omega

        transforms = [
            self.create_transform('odom', 'base_footprint', (-0.3, 0.0, 0.0), (0, 0, 0)),
            self.create_transform('base_link', 'wheel_r', (0.052, -0.095, -0.0025), (0, angle, 0)),
            self.create_transform('base_link', 'wheel_l', (0.052, 0.095, -0.0025), (0, angle, 0)),
        ]

        for t in transforms:
            self.broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = FramePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
