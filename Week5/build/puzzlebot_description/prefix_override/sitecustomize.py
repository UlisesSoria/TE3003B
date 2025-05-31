import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/alexl/test/TE3003B_Integration_of_Robotics_and_Intelligent_Systems_2025/Week5/install/puzzlebot_description'
