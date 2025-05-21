import numpy as np

def compute_gtg_control(x_target, y_target, x_robot, y_robot, theta_robot, min_speed=0.05):
    """
    Computa los comandos de control para navegar hacia un objetivo (Go-To-Goal)
    
    Args:
        x_target, y_target: Coordenadas del objetivo
        x_robot, y_robot: Posición actual del robot
        theta_robot: Orientación actual del robot [rad]
        min_speed: Velocidad lineal mínima para evitar paradas completas
        
    Returns:
        tuple: (velocidad lineal, velocidad angular)
    """
    # Parámetros del controlador
    MAX_LINEAR_SPEED = 0.1  # Velocidad lineal máxima [m/s]
    MAX_ANGULAR_SPEED = 0.4  # Velocidad angular máxima [rad/s]
    LINEAR_GROWTH_RATE = 0.5  # Tasa de crecimiento exponencial para velocidad lineal
    ANGULAR_GROWTH_RATE = 1.0  # Tasa de crecimiento exponencial para velocidad angular
    ANGLE_THRESHOLD = np.pi/8  # Umbral angular para reducir velocidad lineal [rad]
    
    # Calcular distancia al objetivo
    distance = np.sqrt((x_target-x_robot)**2 + (y_target-y_robot)**2)
    
    # Calcular ángulo hacia el objetivo
    target_angle = np.arctan2(y_target-y_robot, x_target-x_robot)
    angle_error = target_angle - theta_robot
    
    # Normalizar error angular entre -π y π
    angle_error = np.arctan2(np.sin(angle_error), np.cos(angle_error))
    
    # Control de velocidad angular (suavizado con función exponencial)
    if abs(angle_error) > 1e-6:  # Evitar división por cero
        kw = MAX_ANGULAR_SPEED * (1 - np.exp(-ANGULAR_GROWTH_RATE * angle_error**2)) / abs(angle_error)
        angular_speed = kw * angle_error
    else:
        angular_speed = 0.0
    
    # Control de velocidad lineal
    if abs(angle_error) > ANGLE_THRESHOLD:
        # Reducir velocidad lineal si no estamos bien alineados
        linear_speed = min_speed
    else:
        # Control proporcional suavizado para velocidad lineal
        if distance > 1e-6:  # Evitar división por cero
            kv = MAX_LINEAR_SPEED * (1 - np.exp(-LINEAR_GROWTH_RATE * distance**2)) / abs(distance)
            linear_speed = max(kv * distance, min_speed)  # Nunca menos que min_speed
        else:
            linear_speed = 0.0
    
    # Limitar velocidades a los máximos permitidos
    linear_speed = np.clip(linear_speed, -MAX_LINEAR_SPEED, MAX_LINEAR_SPEED)
    angular_speed = np.clip(angular_speed, -MAX_ANGULAR_SPEED, MAX_ANGULAR_SPEED)
    
    return linear_speed, angular_speed