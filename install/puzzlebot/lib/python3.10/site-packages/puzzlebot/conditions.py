import numpy as np

def is_point_near_segment(x1, y1, x2, y2, x3, y3, epsilon):
    """
    Determina si un punto (x1,y1) está cerca de un segmento de línea definido por (x2,y2) y (x3,y3)
    
    Args:
        x1, y1: Coordenadas del punto a evaluar
        x2, y2, x3, y3: Coordenadas que definen el segmento de línea
        epsilon: Distancia máxima para considerar "cerca"
        
    Returns:
        tuple: (bool indicando si está cerca, distancia exacta)
    """
    a, b, c = calculate_line_equation(x2, y2, x3, y3)
    numerator = np.abs(a*x1 + b*y1 + c)
    denominator = np.sqrt(a*a + b*b)
    distance = numerator / denominator
    
    if distance <= epsilon:
        return True, distance
    return False, distance

def calculate_line_equation(x1, y1, x2, y2):
    """
    Calcula los coeficientes (a,b,c) de la ecuación de la línea ax + by + c = 0
    que pasa por los puntos (x1,y1) y (x2,y2)
    """
    a = y2 - y1
    b = x1 - x2
    c = x2 * y1 - x1 * y2
    return a, b, c

def quit_wf_bug_two(theta_gtg, theta_ao, xg, yg, x, y, x_init, y_init):
    """
    Determina si el robot debe salir del modo seguidor de pared (Bug 2)
    basado en su posición relativa al segmento inicial y los ángulos
    
    Args:
        theta_gtg: Ángulo hacia el objetivo
        theta_ao: Ángulo de evitación de obstáculos
        xg, yg: Coordenadas del objetivo
        x, y: Coordenadas actuales del robot
        x_init, y_init: Coordenadas iniciales cuando empezó a seguir la pared
        
    Returns:
        bool: True si debe salir del modo seguidor de pared
    """
    n_segment, distance = is_point_near_segment(x, y, x_init, y_init, xg, yg, 0.12)
    
    if (n_segment) and (np.abs(theta_ao - theta_gtg) < np.pi/2) and (np.abs(theta_gtg) < np.pi/2):
        return True
    else:
        return False
        
def quit_wf_bug_two_t(xg, yg, x, y, x_tmp, y_tmp):
    """
    Versión alternativa de la condición de salida para Bug 2
    
    Args:
        xg, yg: Coordenadas del objetivo
        x, y: Coordenadas actuales del robot
        x_tmp, y_tmp: Coordenadas temporales de referencia
        
    Returns:
        bool: True si debe salir del modo seguidor de pared
    """
    d_tmp = np.sqrt((xg - x_tmp)**2 + (yg - y_tmp)**2) - 0.07
    d_r = np.sqrt((xg - x)**2 + (yg - y)**2)
    return d_tmp > d_r

def crash_state(cl_distance, cl_angle, follow_distance):
    """
    Determina si el robot está en peligro de colisión
    
    Args:
        cl_distance: Distancia al obstáculo más cercano
        cl_angle: Ángulo al obstáculo más cercano
        follow_distance: Distancia de seguridad
        
    Returns:
        bool: True si está en peligro de colisión
    """
    distance = cl_distance <= follow_distance
    angle = cl_angle > -np.pi/4 and cl_angle < np.pi/4
    return distance and angle

def quit_wf_bug_zero(theta_gtg, theta_ao, d_t, d_t1):
    """
    Condición de salida para el algoritmo Bug 0
    
    Args:
        theta_gtg: Ángulo hacia el objetivo
        theta_ao: Ángulo de evitación de obstáculos
        d_t: Distancia actual al objetivo
        d_t1: Distancia al objetivo cuando comenzó a seguir la pared
        
    Returns:
        bool: True si debe salir del modo seguidor de pared
    """
    if (d_t < d_t1) and (np.abs(theta_ao - theta_gtg) < np.pi/2):
        return True
    else:
        return False
    
def clockwise_counter(xg, yg, x, y, theta, closest_angle):
    """
    Determina la dirección óptima para rodear un obstáculo (sentido horario/antihorario)
    
    Args:
        xg, yg: Coordenadas del objetivo
        x, y: Coordenadas actuales del robot
        theta: Orientación actual del robot
        closest_angle: Ángulo al obstáculo más cercano
        
    Returns:
        int: 1 para sentido horario, 0 para antihorario
    """
    theta_target = np.arctan2(yg-y, xg-x) 
    e_theta = theta_target-theta
    e_theta = np.arctan2(np.sin(e_theta), np.cos(e_theta)) 

    theta_ao = closest_angle
    theta_ao = np.arctan2(np.sin(theta_ao), np.cos(theta_ao))
    theta_ao = theta_ao - np.pi
    theta_ao = np.arctan2(np.sin(theta_ao), np.cos(theta_ao))

    theta_fw = -np.pi/2 + theta_ao
    theta_fw = np.arctan2(np.sin(theta_fw), np.cos(theta_fw))
    
    if np.abs(theta_fw - e_theta) <= np.pi/2:
        return 1  # Horario
    else:
        return 0  # Antihorario

def compute_angles(xg, yg, x, y, theta, closest_angle):
    """
    Calcula los ángulos relevantes para la navegación
    
    Args:
        xg, yg: Coordenadas del objetivo
        x, y: Coordenadas actuales del robot
        theta: Orientación actual del robot
        closest_angle: Ángulo al obstáculo más cercano
        
    Returns:
        tuple: (ángulo al objetivo, ángulo de evitación de obstáculos)
    """
    theta_target = np.arctan2(yg-y, xg-x) 
    e_theta = theta_target-theta
    e_theta = np.arctan2(np.sin(e_theta), np.cos(e_theta)) 

    theta_ao = closest_angle
    theta_ao = np.arctan2(np.sin(theta_ao), np.cos(theta_ao))
    theta_ao = theta_ao - np.pi
    theta_ao = np.arctan2(np.sin(theta_ao), np.cos(theta_ao))

    return e_theta, theta_ao