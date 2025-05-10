import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/emeryb/ros2_ws/src/equipo6/TE3003B/install/equipo6'
