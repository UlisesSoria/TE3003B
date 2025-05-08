import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/alexl/ActM3.5/TE3003B/equipo6/install/equipo6'
