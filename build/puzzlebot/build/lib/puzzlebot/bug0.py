import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from tf_transformations import euler_from_quaternion
import numpy as np
import math
import signal
import sys
from copy import deepcopy  # Added this import

class Bug0(Node):
    def __init__(self):
        super().__init__('bug0')

        # Publicador al tópico cmd_vel
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)

        # Suscriptores
        self.odom_sub = self.create_subscription(Odometry, 'odom', self.odom_callback, 10)
        self.scan_sub = self.create_subscription(LaserScan, 'scan', self.scan_callback, 10)
        self_goal_sub = self.create_subscription(Odometry, 'goal', self.isGoal_callback, 10)

        # Variables de estado
        self.position = [0.0, 0.0]  # Posición (x, y)
        self.yaw = 0.0
        self.goal = None
        self.obstacle_detected = False
        self.lidar = None

        self.goal_x = 0.0
        self.goal_y = 0.0
        
        # Parámetros de control
        self.min_obstacle_distance = 0.5  # Distancia mínima para considerar un obstáculo
        self.start_fw_distance = 0.5  # Distancia para iniciar el seguimiento de paredes
        self.fw_distance = 0.2  # Distancia deseada a la pared
        self.v_max = 0.5  # Velocidad lineal máxima
        self.w_max = 1.3  # Velocidad angular máxima
        self.kw1 = 2.0  # Ganancia para el control de orientación
        self.kw2 = 3.0  # Ganancia para el control de proximidad

        self.robot_vel = Twist()

        # Configurar manejo de Ctrl+C
        signal.signal(signal.SIGINT, self.shutdown_function)

        # Frecuencia de actualización
        self.timer = self.create_timer(0.1, self.navigate_to_goal)

        self.get_logger().info("Nodo Bug0 mejorado con seguimiento de paredes inicializado.")

    def scan_callback(self, msg):
        """Callback para procesar datos del sensor láser."""
        self.lidar = deepcopy(msg)
        # Reemplazar valores infinitos
        inf_value = 100.0
        for i in range(len(self.lidar.ranges)):
            if np.isinf(self.lidar.ranges[i]):
                self.lidar.ranges[i] = inf_value
                
        self.obstacle_detected = any(distance < self.min_obstacle_distance 
                                    for distance in self.lidar.ranges if distance > 0.0)

    def odom_callback(self, msg):
        """Callback para actualizar la posición y orientación del robot."""
        self.position[0] = msg.pose.pose.position.x
        self.position[1] = msg.pose.pose.position.y

        orientation_q = msg.pose.pose.orientation
        _, _, self.yaw = euler_from_quaternion([orientation_q.x, orientation_q.y, 
                                              orientation_q.z, orientation_q.w])

    def set_goal(self, x, y):
        """Establece el punto objetivo."""
        self.goal = (x, y)

    def distance_to_goal(self):
        """Calcula la distancia al objetivo."""
        if not self.goal:
            return float('inf')
        gx, gy = self.goal
        return math.sqrt((gx - self.position[0])**2 + (gy - self.position[1])**2)

    def angle_to_goal(self):
        """Calcula el ángulo hacia el objetivo."""
        if not self.goal:
            return 0.0
        gx, gy = self.goal
        return math.atan2(gy - self.position[1], gx - self.position[0])

    def follow_wall(self):
        """Lógica mejorada para seguir la pared con detección de esquinas."""
        if not self.lidar:
            return

        closest_range, closest_angle = self.get_closest_object()
        ao_angle = self.get_ao_angle(closest_angle)

        if closest_range > self.start_fw_distance:
            # Si no hay pared cerca, avanza recto
            self.robot_vel.linear.x = self.v_max
            self.robot_vel.angular.z = 0.0
        else:
            # Seguimiento de pared mejorado
            fwcc_angle = self.get_fwcc_angle(ao_angle)
            wfw1 = self.kw1 * fwcc_angle  # Control proporcional para alinearse con la pared
            size = len(self.lidar.ranges)
            left_distance = min(self.lidar.ranges[int(3*size/20):int(5*size/20)])
            proximity_error = left_distance - self.fw_distance
            wfw2 = self.kw2 * proximity_error

            # Detección de regiones para esquinas
            front_region = self.lidar.ranges[int(19*size/20):] + self.lidar.ranges[:int(1*size/20)]
            front_distance = min(front_region)
            front_left_distance = min(self.lidar.ranges[int(1*size/20):int(3*size/20)])
            back_left_distance = min(self.lidar.ranges[int(5*size/20):int(7*size/20)])

            if front_distance < self.fw_distance:  # Esquina interna
                self.get_logger().warn("Inner corner detected, turn right")
                self.robot_vel.linear.x = 0.0
                self.robot_vel.angular.z = -self.w_max
            elif front_distance < self.fw_distance * 2.0:  # Obstáculo cercano al frente
                self.get_logger().warn("Obstacle ahead, slowing down")
                self.robot_vel.linear.x = 0.5 * self.v_max
            elif (back_left_distance < self.start_fw_distance and 
                  left_distance >= self.start_fw_distance and 
                  front_left_distance >= self.start_fw_distance and 
                  front_distance >= self.start_fw_distance):  # Esquina externa
                self.get_logger().warn("Outer corner detected, turn left")
                self.robot_vel.linear.x = self.v_max / 5.0
                self.robot_vel.angular.z = self.w_max
            else:  # Seguimiento normal de pared
                self.robot_vel.linear.x = self.v_max
                self.robot_vel.angular.z = wfw1 + wfw2

        self.cmd_vel_pub.publish(self.robot_vel)

    def navigate_to_goal(self):
        """Navega hacia el objetivo usando Bug0 con seguimiento de paredes mejorado."""
        if not self.goal:
            self.get_logger().warn("El objetivo no ha sido establecido.")
            return

        if self.distance_to_goal() > 0.1:  # Tolerancia de 10 cm
            if self.obstacle_detected:
                self.get_logger().info("Obstáculo detectado, siguiendo la pared.")
                self.follow_wall()
            else:
                angle_to_goal = self.angle_to_goal()
                angle_error = angle_to_goal - self.yaw

                # Normalizar el ángulo entre -pi y pi
                angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))

                twist = Twist()
                if abs(angle_error) > 0.1:  # Si hay un error angular significativo
                    twist.angular.z = 0.5 * angle_error
                else:
                    twist.linear.x = 0.2  # Avanza hacia el objetivo

                self.cmd_vel_pub.publish(twist)
        else:
            self.get_logger().info("¡Objetivo alcanzado!")
            self.stop_robot()

    def stop_robot(self):
        """Detiene el robot."""
        twist = Twist()
        self.cmd_vel_pub.publish(twist)
        rclpy.shutdown()

    def get_closest_object(self):
        """Obtiene el objeto más cercano del sensor láser."""
        if not self.lidar:
            return (float('inf'), 0.0)
            
        closest_range = min(self.lidar.ranges)
        closest_index = self.lidar.ranges.index(closest_range)
        closest_angle = self.lidar.angle_min + closest_index * self.lidar.angle_increment
        closest_angle = np.arctan2(np.sin(closest_angle), np.cos(closest_angle))
        return closest_range, closest_angle

    def get_ao_angle(self, closest_angle):
        """Calcula el ángulo de alejamiento del obstáculo."""
        ao_angle = closest_angle + np.pi
        return np.arctan2(np.sin(ao_angle), np.cos(ao_angle))

    def get_fwcc_angle(self, closest_angle):
        """Calcula el ángulo de corrección para seguir la pared."""
        fwcc_angle = closest_angle + np.pi / 2
        return np.arctan2(np.sin(fwcc_angle), np.cos(fwcc_angle))

    def shutdown_function(self, signum, frame):
        """Maneja la señal Ctrl+C para detener el robot y cerrar el nodo."""
        self.get_logger().info("Ctrl+C pressed. Stopping robot...")
        self.stop_robot()
        rclpy.shutdown()
        sys.exit(0)

    def isGoal_callback(self, msg):
        """Callback para recibir el objetivo."""
        self.goal_x = msg.pose.pose.position.x
        self.goal_y = msg.pose.pose.position.y
        self.get_logger().info(f"Nuevo objetivo recibido: ({self.goal_x}, {self.goal_y})")
        if self.goal_x == 1.45 and self.goal_y == 1.2:
            self.get_logger().info("Objetivo alcanzado (1.45, 1.2).")
            self.stop_robot()

def main(args=None):
    rclpy.init(args=args)

    controller = Bug0()
    controller.set_goal(1.45, 1.2)  # Establece el objetivo

    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        controller.get_logger().info("Nodo detenido por el usuario.")
    finally:
        controller.stop_robot()
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()