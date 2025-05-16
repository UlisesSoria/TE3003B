#!/usr/bin/env python3
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

        self.namespace = self.get_namespace().rstrip('/')
        
        self.tf_br1 = StaticTransformBroadcaster(self)
        self.tf_br2 = StaticTransformBroadcaster(self)
        self.tf_br3 = StaticTransformBroadcaster(self)
        self.tf_br4 = StaticTransformBroadcaster(self)

        self.declare_parameter('frame', 'odom')

        self.odom_frame = self.get_parameter('frame').value
        self.x = self.get_parameter('x').value
        self.y = self.get_parameter('y').value
        self.z = self.get_parameter('z').value

        self.cmd_vel_subscriber = self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_callback, 10) 
        self.tf_broadcaster = TransformBroadcaster(self)
        self.subscription = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)

        self.r = 0.05 #puzzlebot wheel radius [m] 
        self.L = 0.19 #puzzlebot wheel separation [m] 

        self.v = 0.0
        self.w = 0.0

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


        self.t2 = TransformStamped()
        self.t3 = TransformStamped()
        self.t4 = TransformStamped()
        #Create a Timer
        timer_period = 0.01 #seconds
        self.timer = self.create_timer(timer_period, self.timer_cb)
        #Variables to be used
        self.start_time = self.get_clock().now()
        
        self.tf_br1.sendTransform(t)

    def cmd_vel_callback(self, msg):
        self.w = msg.angular.z 
        self.v = msg.linear.x

    def timer_cb(self):
        
        wr,wl = self.get_wheel_speeds()

        elapsed_time = (self.get_clock().now() - self.start_time).nanoseconds/1e9

        self.t2.header.stamp = self.get_clock().now().to_msg()
        self.t2.header.frame_id = self.odom_frame
        self.t2.child_frame_id = 'base_footprint'
        self.t2.transform.translation.x = self.x
        self.t2.transform.translation.y = self.y
        self.t2.transform.translation.z = self.z
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
        q = transforms3d.euler.euler2quat(0, wl * elapsed_time, 0)      
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
        q = transforms3d.euler.euler2quat(0, wr * elapsed_time, 0)
        self.t4.transform.rotation.x = q[1]
        self.t4.transform.rotation.y = q[2]
        self.t4.transform.rotation.z = q[3]
        self.t4.transform.rotation.w = q[0]

        # Send the transform
        self.tf_br2.sendTransform(self.t2)
        self.tf_br3.sendTransform(self.t3)
        self.tf_br4.sendTransform(self.t4)

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

    def get_wheel_speeds(self): 

        # Calculate the wheel speeds based on the linear and angular velocities 

        wr = 0.0 

        wl = 0.0 

        wr = (2*self.v + self.w*self.L)/(2*self.r)

        wl = (2*self.v - self.w*self.L)/(2*self.r)

        if (wr == 0 and wl == 0):
            
            wr = self.v + (self.w*self.L)/2
            
            wl = self.v - (self.w*self.L)/2

        return wr, wl 

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