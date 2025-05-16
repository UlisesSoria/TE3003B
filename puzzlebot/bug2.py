import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from tf_transformations import euler_from_quaternion
import numpy as np
import math

class ImprovedBug2(Node):
    def __init__(self):
        super().__init__('improved_bug2')
        
        # Suscriptores y publicadores
        self.sub_laser = self.create_subscription(LaserScan, 'scan', self.laser_cb, 10)
        self.sub_odom = self.create_subscription(Odometry, 'odom', self.odom_cb, 10)
        self.pub_cmd_vel = self.create_publisher(Twist, 'cmd_vel', 10)
        
        # Timer de control
        self.timer = self.create_timer(0.1, self.loop_callback)
        
        # Parámetros del objetivo
        self.xg = 1.46
        self.yg = 1.20
        self.goal_reached = False
        self.lidar_ready = False

        # Variables de estado
        self.e_theta = 0.0
        self.theta_ao = 0.0
        self.theta_fw = 0.0
        self.xr = 0.0
        self.yr = 0.0
        self.tr = 0.0  # Orientación del robot
        self.closest_angle = 0.0
        self.closest_range = np.inf
        self.hit_point = None
        self.leave_point = None
        
        # Parámetros de control
        self.tolerance = 0.1  # Tolerancia para alcanzar el objetivo
        self.following_distance = 0.4  # Distancia para seguir paredes
        self.safety_distance = 0.5  # Distancia de seguridad para obstáculos
        self.m_line_tolerance = 0.1  # Tolerancia para estar en la línea m
        self.min_progress = 0.3  # Progreso mínimo para considerar avance
        
        # Control de velocidad
        self.v = 0.0
        self.w = 0.0
        self.max_linear_speed = 0.3
        self.max_angular_speed = 1.3
        
        # Estados del algoritmo
        self.current_state = 'GTG'  # 'GTG', 'CW', 'CCW', 'STOP'
        self.previous_distance_to_goal = np.inf
        
        # Mensaje de velocidad
        self.vel_msg = Twist()

    def loop_callback(self):
        if not self.lidar_ready or self.goal_reached:
            return

        self.get_closest_range()
        
        if self.at_goal():
            self.get_logger().info("Objetivo alcanzado!")
            self.current_state = 'STOP'
            self.v = 0.0
            self.w = 0.0
            self.goal_reached = True
        else:
            self.fsm_controller()
        
        self.vel_msg.linear.x = self.v
        self.vel_msg.angular.z = self.w
        self.pub_cmd_vel.publish(self.vel_msg)

    def fsm_controller(self):
        """Máquina de estados finitos mejorada"""
        distance_to_goal = self.distance_to_goal()
        
        if self.current_state == 'GTG':
            self.gtg_control()
            
            # Transición a seguir pared si detecta obstáculo
            if self.closest_range <= self.following_distance:
                self.hit_point = (self.xr, self.yr)
                self.previous_distance_to_goal = distance_to_goal
                
                # Decide dirección para seguir la pared
                if self.closest_angle >= 0:
                    self.current_state = 'CCW'  # Sentido antihorario
                else:
                    self.current_state = 'CW'  # Sentido horario
                
                self.get_logger().info(f"Obstáculo detectado. Siguiendo pared en dirección {'CCW' if self.current_state == 'CCW' else 'CW'}")
        
        elif self.current_state in ['CW', 'CCW']:
            clockwise = (self.current_state == 'CW')
            self.fw_control(clockwise)
            
            # Condiciones para volver a GTG
            if self.on_m_line() and self.is_closer_to_goal():
                if not self.obstacle_ahead():
                    self.current_state = 'GTG'
                    self.get_logger().info("Volviendo a la línea m. Reanudando navegación directa.")
                else:
                    self.get_logger().info("Obstáculo detectado en la línea m. Continuando seguimiento de pared.")
            
            # Condición de fallo (estancamiento)
            elif distance_to_goal > self.previous_distance_to_goal + self.min_progress:
                self.get_logger().warn("Estancamiento detectado. Cambiando dirección.")
                self.current_state = 'CCW' if self.current_state == 'CW' else 'CW'
            
            self.previous_distance_to_goal = distance_to_goal

    def at_goal(self):
        """Verifica si el robot ha alcanzado el objetivo"""
        return math.hypot(self.xg - self.xr, self.yg - self.yr) < self.tolerance

    def distance_to_goal(self):
        """Calcula la distancia al objetivo"""
        return math.hypot(self.xg - self.xr, self.yg - self.yr)

    def on_m_line(self):
        """Determina si el robot está en la línea m con mayor precisión"""
        # Ecuación de la línea desde inicio (0,0) a objetivo (xg, yg): (yg)x - (xg)y = 0
        a = self.yg
        b = -self.xg
        c = 0
        
        # Distancia perpendicular a la línea
        distance = abs(a * self.xr + b * self.yr + c) / math.hypot(a, b)
        
        # Verificar también que esté entre el inicio y el objetivo
        dot_product = (self.xr * (self.xg - 0) + self.yr * (self.yg - 0)) / (self.xg**2 + self.yg**2)
        between_points = 0 <= dot_product <= 1
        
        return distance <= self.m_line_tolerance and between_points

    def is_closer_to_goal(self):
        """Verifica si el robot está más cerca del objetivo que cuando encontró el obstáculo"""
        if not self.hit_point:
            return False
            
        current_distance = self.distance_to_goal()
        hit_distance = math.hypot(self.xg - self.hit_point[0], self.yg - self.hit_point[1])
        
        return current_distance < hit_distance - self.min_progress

    def obstacle_ahead(self):
        """Verifica si hay obstáculos en la dirección del objetivo"""
        if not hasattr(self, 'lidar_msg'):
            return False
            
        angle_to_goal = math.atan2(self.yg - self.yr, self.xg - self.xr)
        angle_error = angle_to_goal - self.tr
        angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))
        
        # Buscar en un cono de ±30 grados hacia el objetivo
        angle_range = math.radians(30)
        angle_min = angle_error - angle_range
        angle_max = angle_error + angle_range
        
        ranges = []
        for i, distance in enumerate(self.lidar_msg.ranges):
            angle = self.lidar_msg.angle_min + i * self.lidar_msg.angle_increment
            if angle_min <= angle <= angle_max and distance > 0:
                ranges.append(distance)
        
        if not ranges:
            return False
            
        return min(ranges) < self.safety_distance

    def get_closest_range(self):
        """Obtiene el obstáculo más cercano y su ángulo"""
        if not hasattr(self, 'lidar_msg'):
            return
            
        valid_ranges = [(i, r) for i, r in enumerate(self.lidar_msg.ranges) if r > 0]
        if not valid_ranges:
            self.closest_range = np.inf
            return
            
        min_idx, min_range = min(valid_ranges, key=lambda x: x[1])
        self.closest_range = min_range
        self.closest_angle = self.lidar_msg.angle_min + min_idx * self.lidar_msg.angle_increment
        self.closest_angle = math.atan2(math.sin(self.closest_angle), math.cos(self.closest_angle))

    def gtg_control(self):
        """Control para ir directamente al objetivo"""
        kv = 0.5
        kw = 1.0
        
        dx = self.xg - self.xr
        dy = self.yg - self.yr
        distance = math.hypot(dx, dy)
        angle_to_goal = math.atan2(dy, dx)
        angle_error = angle_to_goal - self.tr
        angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))
        
        # Control de velocidad angular
        self.w = kw * angle_error
        
        # Control de velocidad lineal (solo avanzar si está alineado)
        if abs(angle_error) < math.radians(20):
            self.v = kv * distance
            if self.v > self.max_linear_speed:
                self.v = self.max_linear_speed
        else:
            self.v = 0.0

    def fw_control(self, clockwise):
        """Control para seguir la pared"""
        kw = 1.8
        desired_distance = self.following_distance
        
        # Ángulo para seguir la pared (90° respecto al obstáculo más cercano)
        if clockwise:
            follow_angle = self.closest_angle - math.pi/2
        else:
            follow_angle = self.closest_angle + math.pi/2
        
        # Normalizar ángulo
        follow_angle = math.atan2(math.sin(follow_angle), math.cos(follow_angle))
        
        # Control de velocidad angular
        self.w = kw * follow_angle
        
        # Control de velocidad lineal (reducir si hay obstáculos al frente)
        front_angle_range = math.radians(30)
        front_distances = []
        for i, distance in enumerate(self.lidar_msg.ranges):
            angle = self.lidar_msg.angle_min + i * self.lidar_msg.angle_increment
            if -front_angle_range <= angle <= front_angle_range and distance > 0:
                front_distances.append(distance)
        
        if front_distances:
            min_front_distance = min(front_distances)
            if min_front_distance < self.safety_distance:
                self.v = 0.1 * self.max_linear_speed
            else:
                self.v = 0.5 * self.max_linear_speed
        else:
            self.v = 0.3 * self.max_linear_speed

    def laser_cb(self, msg):
        self.lidar_msg = msg
        self.lidar_ready = True

    def odom_cb(self, msg):
        orientation = [
            msg.pose.pose.orientation.x,
            msg.pose.pose.orientation.y,
            msg.pose.pose.orientation.z,
            msg.pose.pose.orientation.w
        ]
        _, _, self.tr = euler_from_quaternion(orientation)
        self.xr = msg.pose.pose.position.x
        self.yr = msg.pose.pose.position.y

def main(args=None):
    rclpy.init(args=args)
    controller = ImprovedBug2()
    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        pass
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()