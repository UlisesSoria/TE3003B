import numpy as np
from .pid import PIDController 

class WallFollower:
    def __init__(self):
        """
        Inicializa los controladores PID para el seguimiento de pared.
        """
        # Controladores PID preconfigurados
        self.angle_pid = PIDController(Kp=2.4, Ki=0.0015, Kd=0.001)
        self.distance_pid = PIDController(Kp=0.9, Ki=0.001, Kd=0.001)
        
        # Parámetros fijos
        self.base_speed = 0.08  # Velocidad lineal base [m/s]
        self.angle_offset = np.pi/2  # 90 grados para seguimiento perpendicular

    def normalize_angle(self, angle):
        """
        Normaliza un ángulo al rango [-π, π].
        """
        return np.arctan2(np.sin(angle), np.cos(angle))

    def compute_wf_control(self, closest_angle, distance_to_wall, target_distance, clockwise, dt):
        """
        Calcula los comandos de control para el seguimiento de pared.
        
        Args:
            closest_angle: Ángulo al punto más cercano de la pared [rad]
            distance_to_wall: Distancia actual a la pared [m]
            target_distance: Distancia deseada a la pared [m]
            clockwise: Sentido de giro (True=horario, False=antihorario)
            dt: Paso de tiempo [s]
            
        Returns:
            tuple: (velocidad lineal, velocidad angular)
        """
        # Normalizar ángulo de la pared
        theta_ao = self.normalize_angle(closest_angle)
        
        # Calcular dirección óptima de seguimiento
        direction = 1 if clockwise else -1
        theta_fw = direction * self.angle_offset + theta_ao
        theta_fw = self.normalize_angle(theta_fw)
        
        # Control de ángulo (mantener dirección de seguimiento)
        angle_control = self.angle_pid.compute(theta_fw, dt)
        
        # Control de distancia (mantener distancia a la pared)
        distance_error = distance_to_wall - target_distance
        distance_control = self.distance_pid.compute(distance_error, dt)
        
        # Velocidad angular combinada
        w_fw = angle_control + distance_control
        
        return self.base_speed, w_fw

# Función de compatibilidad (misma interfaz que la versión original)
def compute_wf_controller(closest_angle, distance_to_wall, target_distance, clockwise, dt):
    """
    Versión funcional del controlador para mantener compatibilidad.
    """
    controller = WallFollower()
    return controller.compute_wf_control(
        closest_angle=closest_angle,
        distance_to_wall=distance_to_wall,
        target_distance=target_distance,
        clockwise=bool(clockwise),
        dt=dt
    )