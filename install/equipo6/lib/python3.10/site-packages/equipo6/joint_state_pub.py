import rclpy
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster, TransformBroadcaster
from geometry_msgs.msg import TransformStamped, Twist
import transforms3d
from nav_msgs.msg import Odometry
import numpy as np

class PuzzlebotTFBroadcaster(Node):
    def __init__(self):
        super().__init__('joint_state_pub')

        self.declare_parameter('frame', 'odom')

        self.odom_frame = self.get_parameter('frame').value
        
        self.tf_br1 = StaticTransformBroadcaster(self)
        self.tf_br2 = StaticTransformBroadcaster(self)
        self.tf_br3 = StaticTransformBroadcaster(self)

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'map'
        t.child_frame_id = self.odom_frame
        t.transform.translation.x = 0.0
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.0
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        q = transforms3d.euler.euler2quat(0, 0, 0)      #input euler2quat(roll, pitch, yaw) , output q=[w, x, y, z] 
        t.transform.rotation.x = q[1]
        t.transform.rotation.y = q[2]
        t.transform.rotation.z = q[3]
        t.transform.rotation.w = q[0]

        t2 = TransformStamped()
        t2.header.stamp = self.get_clock().now().to_msg()
        t2.header.frame_id = 'world'
        t2.child_frame_id = 'map'
        t2.transform.translation.x = 0.0
        t2.transform.translation.y = 0.0
        t2.transform.translation.z = 0.0
        t2.transform.rotation.x = 0.0
        t2.transform.rotation.y = 0.0
        t2.transform.rotation.z = 0.0
        q2 = transforms3d.euler.euler2quat(0, 0, 0)      #input euler2quat(roll, pitch, yaw) , output q=[w, x, y, z]
        t2.transform.rotation.x = q2[1]
        t2.transform.rotation.y = q2[2]
        t2.transform.rotation.z = q2[3]
        t2.transform.rotation.w = q2[0]
        
        
        self.tf_br1.sendTransform(t)
        self.tf_br2.sendTransform(t2)
        
        #Create a timer to publish the transform
        self.timer = self.create_timer(0.1, self.publish_transform)

    def publish_transform(self):
        t3 = TransformStamped()
        t3.header.stamp = self.get_clock().now().to_msg()
        t3.header.frame_id = self.odom_frame
        t3.child_frame_id = 'base_footprint'
        t3.transform.translation.x = 0.0
        t3.transform.translation.y = 0.0
        t3.transform.translation.z = 0.0
        q = transforms3d.euler.euler2quat(0, 0, 0)      #input euler2quat(roll, pitch, yaw) , output q=[w, x, y, z] 
        t3.transform.rotation.x = q[1]
        t3.transform.rotation.y = q[2]
        t3.transform.rotation.z = q[3]
        t3.transform.rotation.w = q[0]

        self.tf_br3.sendTransform(t3)

def main(args=None):
    rclpy.init(args=args)

    node = PuzzlebotTFBroadcaster()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():  # Ensure shutdown is only called once
            rclpy.shutdown()
        node.destroy_node()


if __name__ == '__main__':
    main()