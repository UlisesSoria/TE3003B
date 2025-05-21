#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
import transforms3d
import math

class OneTimeOdomPublisher(Node):
    def __init__(self):
        super().__init__('one_time_odom_publisher')
        
        # Crear publisher para odometría
        self.odom_pub = self.create_publisher(Odometry, 'goal', 10)
        
        # Publicar mensaje una sola vez después de 1 segundo (para asegurar conexiones)
        self.timer = self.create_timer(1.0, self.publish_once)
        self.published = False

    def publish_once(self):
        if not self.published:
            # Crear mensaje de odometría
            odom_msg = Odometry()
            
            # Configurar header
            odom_msg.header.stamp = self.get_clock().now().to_msg()
            odom_msg.header.frame_id = 'odom'
            odom_msg.child_frame_id = 'base_link'
            
            # Posición (x, y, z)
            odom_msg.pose.pose.position.x = 1.45  # [m]
            odom_msg.pose.pose.position.y = 1.2  # [m]
            odom_msg.pose.pose.position.z = 0.0  # [m]
            
            # Orientación (cuaternión desde ángulos de Euler)
            # Ángulo de yaw de 45 grados (π/4 radianes)
            roll = 0.0
            pitch = 0.0
            yaw = 0.0
            q = transforms3d.euler.euler2quat(roll, pitch, yaw)
            
            odom_msg.pose.pose.orientation = Quaternion(
                x=q[1],  # Componente i
                y=q[2],  # Componente j
                z=q[3],  # Componente k
                w=q[0]   # Componente real
            )
            
            # Covarianza (6x6, solo diagonal para este ejemplo)
            odom_msg.pose.covariance = [
                0.1, 0.0, 0.0, 0.0, 0.0, 0.0,  # var x
                0.0, 0.1, 0.0, 0.0, 0.0, 0.0,  # var y
                0.0, 0.0, 0.1, 0.0, 0.0, 0.0,  # var z
                0.0, 0.0, 0.0, 0.1, 0.0, 0.0,  # var rot x
                0.0, 0.0, 0.0, 0.0, 0.1, 0.0,  # var rot y
                0.0, 0.0, 0.0, 0.0, 0.0, 0.1   # var rot z
            ]
            
            # Velocidad (opcional)
            odom_msg.twist.twist.linear.x = 0.2  # [m/s]
            odom_msg.twist.twist.angular.z = 0.1  # [rad/s]
            
            # Publicar mensaje
            self.odom_pub.publish(odom_msg)
            self.get_logger().info('Mensaje de odometría publicado una vez')
            
            # Marcar como publicado y cerrar el nodo
            self.published = True
            self.timer.cancel()
            rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = OneTimeOdomPublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()