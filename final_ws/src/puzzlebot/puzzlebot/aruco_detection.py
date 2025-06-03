import rclpy
from rclpy.node import Node
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from std_msgs.msg import Bool, Float32MultiArray
from geometry_msgs.msg import PoseStamped
import numpy as np
from geometry_msgs.msg import TransformStamped
import transforms3d

class ArucoDetector(Node):
    def __init__(self):
        super().__init__('aruco_detector')
        
        # Configuración de TF
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        # Configuración de marcadores conocidos (posición en odom)
        self.marker_positions = {
            0: (2.5, -0.5, -np.pi),  # (x, y, theta) en odom frame
            1: (2.5, 2.5, -np.pi/2),
            2: (-0.5, 2.5, 0.0),
            3: (-0.5, -0.5, np.pi/2),
        }
        
        # Publishers
        self.detection_flag_pub = self.create_publisher(Bool, 'aruco_detection_flag', 10)
        self.marker_position_pub = self.create_publisher(Float32MultiArray, 'marker_position_odom', 10)
        self.robot_transform_pub = self.create_publisher(Float32MultiArray, 'robot_transform_to_marker', 10)
        
        # Temporizador para la detección
        self.timer = self.create_timer(0.1, self.detect_markers)
        
        self.get_logger().info("Aruco Detector Node has been started")

    def detect_markers(self):
        detected = False
        parent_frame = 'base_link'
        
        for marker_id in self.marker_positions.keys():
            child_frame = f'marker_{marker_id}'
            try:
                # Obtener transformación del marcador al robot
                transform = self.tf_buffer.lookup_transform(
                    parent_frame, child_frame, rclpy.time.Time())
                
                # Publicar flag de detección
                flag_msg = Bool()
                flag_msg.data = True
                self.detection_flag_pub.publish(flag_msg)
                detected = True
                
                # Publicar posición del marcador en odom
                marker_x, marker_y, marker_theta = self.marker_positions[marker_id]
                marker_pos_msg = Float32MultiArray()

                
                marker_pos_msg.data = [float(marker_id), marker_x, marker_y]
                self.marker_position_pub.publish(marker_pos_msg)
                
                # Calcular y publicar matriz de transformación del robot respecto al marcador
                transform_matrix = self.transform_to_matrix(transform)
                transform_msg = Float32MultiArray()
                transform_msg.data = transform_matrix.flatten().tolist()
                self.robot_transform_pub.publish(transform_msg)
                
                self.get_logger().info(f"Detected marker {marker_id}", throttle_duration_sec=1)
                
            except TransformException:
                continue
        
        if not detected:
            flag_msg = Bool()
            flag_msg.data = False
            self.detection_flag_pub.publish(flag_msg)

    def transform_to_matrix(self, transform):
        # Convertir transformación geométrica a matriz 4x4
        translation = np.array([
            transform.transform.translation.x,
            transform.transform.translation.y,
            transform.transform.translation.z
        ])
        
        rotation = [
            transform.transform.rotation.x,
            transform.transform.rotation.y,
            transform.transform.rotation.z,
            transform.transform.rotation.w
        ]
        
        # Matriz de rotación 3x3
        rot_matrix = transforms3d.quaternions.quat2mat(rotation)
        
        # Matriz de transformación homogénea 4x4
        transform_matrix = np.eye(4)
        transform_matrix[:3, :3] = rot_matrix
        transform_matrix[:3, 3] = translation
        
        return transform_matrix

def main(args=None):
    rclpy.init(args=args)
    node = ArucoDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()