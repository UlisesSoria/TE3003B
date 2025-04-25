import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import numpy as np
import transforms3d

class Controller(Node):
    def __init__(self):
        super().__init__('controller')

        # List of goal positions (x, y) without orientation
        self.goals = [
            (1.0, 0.0),
            (1.0, 1.0),
            (0.0, 1.0),
            (0.0, 0.0)
        ]
        self.current_goal_index = 0

        # Control gains
        self.k_rho = 0.7
        self.k_alpha = 1.5

        # Tolerances
        self.orientation_tolerance = 0.1   # rad
        self.position_tolerance = 0.05     # m

        # Publisher and subscriber
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.create_subscription(Odometry, 'odom', self.odom_callback, 10)

    def odom_callback(self, msg):
        # Stop if all goals are reached
        if self.current_goal_index >= len(self.goals):
            return

        # Get robot current pose
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        _, _, theta = transforms3d.euler.quat2euler([q.w, q.x, q.y, q.z])

        # Get current goal
        x_goal, y_goal = self.goals[self.current_goal_index]

        # Calculate errors
        dx = x_goal - x
        dy = y_goal - y
        rho = np.hypot(dx, dy)  # distance to goal
        angle_to_goal = np.arctan2(dy, dx)
        alpha = self.normalize_angle(angle_to_goal - theta)

        # Velocity command
        cmd = Twist()

        if rho < self.position_tolerance:
            # Goal reached, move to the next one
            self.get_logger().info(f"Goal {self.current_goal_index+1} reached.")
            self.current_goal_index += 1
            
            # If it was the last goal, send stop command
            if self.current_goal_index >= len(self.goals):
                stop_cmd = Twist()
                self.cmd_pub.publish(stop_cmd)
            return

        elif abs(alpha) > self.orientation_tolerance:
            # Align to goal
            cmd.linear.x = 0.0
            cmd.angular.z = self.k_alpha * alpha
        else:
            # Go to goal
            cmd.linear.x = self.k_rho * rho
            cmd.angular.z = 0.0

            # Ensure a minimum speed for responsiveness
            if cmd.linear.x < 0.02:
                cmd.linear.x = 0.02

        self.cmd_pub.publish(cmd)

    def normalize_angle(self, angle):
        # Normalize angle to the range [-pi, pi]
        return np.arctan2(np.sin(angle), np.cos(angle))

def main(args=None):
    rclpy.init(args=args)
    node = Controller()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            rclpy.shutdown()
        node.destroy_node()

if __name__ == '__main__':
    main()
