#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped
import transforms3d
import numpy as np

class PuzzlebotTFBroadcaster(Node):
    def __init__(self):
        super().__init__('minichallenge1')
        
        self.tf_br1 = StaticTransformBroadcaster(self)
        self.tf_br2 = StaticTransformBroadcaster(self)
        self.tf_br3 = StaticTransformBroadcaster(self)
        self.tf_br4 = StaticTransformBroadcaster(self)

        
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'map'
        t.child_frame_id = 'odom'
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


        self.t2 = TransformStamped()
        self.t3 = TransformStamped()
        self.t4 = TransformStamped()
        #Create a Timer
        timer_period = 0.01 #seconds
        self.timer = self.create_timer(timer_period, self.timer_cb)
        #Variables to be used
        self.start_time = self.get_clock().now()
        self.omega = 1
        
        self.tf_br1.sendTransform(t)

    def timer_cb(self):
        
        elapsed_time = (self.get_clock().now() - self.start_time).nanoseconds/1e9

        self.t2.header.stamp = self.get_clock().now().to_msg()
        self.t2.header.frame_id = 'odom'
        self.t2.child_frame_id = 'base_footprint'
        self.t2.transform.translation.x = 1.0
        self.t2.transform.translation.y = 0.0
        self.t2.transform.translation.z = 0.0
        q = transforms3d.euler.euler2quat(0, 0, 0)       
        self.t2.transform.rotation.x = q[1]
        self.t2.transform.rotation.y = q[2]
        self.t2.transform.rotation.z = q[3]
        self.t2.transform.rotation.w = q[0]

        self.t3.header.stamp = self.get_clock().now().to_msg()
        self.t3.header.frame_id = 'base_link'
        self.t3.child_frame_id = 'wheel_l'
        self.t3.transform.translation.x = 0.052
        self.t3.transform.translation.y = -0.095
        self.t3.transform.translation.z = -0.0025
        q = transforms3d.euler.euler2quat(0, self.omega * elapsed_time, 0)      
        self.t3.transform.rotation.x = q[1]
        self.t3.transform.rotation.y = q[2]
        self.t3.transform.rotation.z = q[3]
        self.t3.transform.rotation.w = q[0]

        self.t4.header.stamp = self.get_clock().now().to_msg()
        self.t4.header.frame_id = 'base_link'
        self.t4.child_frame_id = 'wheel_r'
        self.t4.transform.translation.x = 0.052
        self.t4.transform.translation.y = 0.095
        self.t4.transform.translation.z = -0.0025
        q = transforms3d.euler.euler2quat(0, self.omega * elapsed_time, 0)
        self.t4.transform.rotation.x = q[1]
        self.t4.transform.rotation.y = q[2]
        self.t4.transform.rotation.z = q[3]
        self.t4.transform.rotation.w = q[0]

        # Send the transform
        self.tf_br2.sendTransform(self.t2)
        self.tf_br3.sendTransform(self.t3)
        self.tf_br4.sendTransform(self.t4)

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