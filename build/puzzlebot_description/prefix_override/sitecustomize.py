import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/ulisess/TE3003B/modulo_3/ActFinal/install/puzzlebot_description'
