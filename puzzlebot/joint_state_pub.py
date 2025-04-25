#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
import numpy as np

class JointTFPublisherFromOdom(Node):
    def __init__(self):
        super().__init__('joint_state_publisher')
        
        self.tf_broadcaster = TransformBroadcaster(self)
        self.subscription = self.create_subscription(Odometry, 'odom', self.odom_callback, 10)

    def odom_callback(self, msg):
        # Extract position
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        z = msg.pose.pose.position.z

        # Extract orientation
        q = msg.pose.pose.orientation

        # Create & publish the transform from odom to base_link
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'base_footprint'
        t.child_frame_id = 'base_link'
        t.transform.translation.x = x
        t.transform.translation.y = y
        t.transform.translation.z = z  # Adjust z position if needed
        t.transform.rotation = q

        self.tf_broadcaster.sendTransform(t)

def main(args=None):
    rclpy.init(args=args)
    node = JointTFPublisherFromOdom()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            rclpy.shutdown()
        node.destroy_node()

if __name__ == '__main__':
    main()
