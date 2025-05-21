import numpy as np

class PIDController:
    def __init__(self, Kp=1.0, Ki=0.0, Kd=0.0, setpoint=0.0,
                 output_limits=(None, None), anti_windup=True,
                 time_fn=None):
        """
        Controlador PID mejorado con características avanzadas.
        
        Args:
            Kp: Ganancia proporcional
            Ki: Ganancia integral
            Kd: Ganancia derivativa
            setpoint: Valor deseado (puede cambiarse después)
            output_limits: Tupla (min, max) para limitar la salida
            anti_windup: Activar/desactivar protección contra windup integral
            time_fn: Función para obtener el tiempo actual (útil para simulaciones)
        """
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        
        # Variables de estado
        self._integral = 0.0
        self._prev_error = 0.0
        self._prev_time = None
        self._last_output = None
        
        # Configuración avanzada
        self.output_limits = output_limits
        self.anti_windup = anti_windup
        self.time_fn = time_fn if time_fn is not None else self._default_time_fn
        
        # Estadísticas
        self._error_history = []
        self.max_history = 1000

    def _default_time_fn(self):
        """Función por defecto para obtener el tiempo actual."""
        import time
        return time.monotonic()

    def reset(self):
        """Reinicia el estado del controlador."""
        self._integral = 0.0
        self._prev_error = 0.0
        self._prev_time = None
        self._last_output = None
        self._error_history = []

    def compute(self, process_variable, dt=None):
        """
        Calcula la salida del controlador PID.
        
        Args:
            process_variable: Valor actual del proceso
            dt: Paso de tiempo (si None, se calcula automáticamente)
            
        Returns:
            float: Valor de control calculado
        """
        error = self.setpoint - process_variable
        current_time = self.time_fn()
        
        # Calcular dt si no se proporciona
        if dt is None:
            if self._prev_time is None:
                dt = 0.0
            else:
                dt = current_time - self._prev_time
        self._prev_time = current_time
        
        # Actualizar términos
        p_term = self.Kp * error
        
        # Término integral con anti-windup
        self._integral += error * dt
        if self.anti_windup and self.output_limits[0] is not None and self.output_limits[1] is not None:
            if self._last_output is not None:
                if (self._last_output >= self.output_limits[1] and error > 0) or \
                   (self._last_output <= self.output_limits[0] and error < 0):
                    self._integral -= error * dt  # Anti-windup
        
        i_term = self.Ki * self._integral
        
        # Término derivativo (protección contra dt=0)
        if dt > 1e-6:
            d_term = self.Kd * (error - self._prev_error) / dt
        else:
            d_term = 0.0
        
        # Calcular salida
        output = p_term + i_term + d_term
        
        # Aplicar límites de salida
        if self.output_limits[0] is not None:
            output = max(self.output_limits[0], output)
        if self.output_limits[1] is not None:
            output = min(self.output_limits[1], output)
        
        # Actualizar estado
        self._prev_error = error
        self._last_output = output
        
        # Guardar historial (para depuración)
        self._error_history.append((current_time, error))
        if len(self._error_history) > self.max_history:
            self._error_history.pop(0)
        
        return output

    def get_history(self):
        """Devuelve el historial de errores para análisis."""
        return np.array(self._error_history)

    def tune(self, Kp=None, Ki=None, Kd=None):
        """Ajusta las ganancias del controlador."""
        if Kp is not None:
            self.Kp = Kp
        if Ki is not None:
            self.Ki = Ki
        if Kd is not None:
            self.Kd = Kd
        self.reset()

    def __call__(self, process_variable, dt=None):
        """Permite usar la instancia como función."""
        return self.compute(process_variable, dt)