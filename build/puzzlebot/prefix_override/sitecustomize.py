import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/ulisess/TE3003B/minichallenges/TE3003B/install/puzzlebot'
