import numpy as np
import transforms3d as t3d

from geometry_msgs.msg import Pose2D, TransformStamped

np.atan2 = np.arctan2 # Ensure compatibility with humble

def get_normalized_angle(angle: float) -> float:
    """Normalize an angle to be between -pi and pi.
    
    Args:
        angle (float): The angle to normalize.
        
    Returns:
        float: The normalized angle.
    """
    return np.atan2(np.sin(angle), np.cos(angle))

def symmetric_theta_shift(theta: float) -> float:
    """Shift an angle from (-pi, pi) to (0, 2*pi).
    
    Args:
        theta (float): The angle to shift.
        
    Returns:
        float: The shifted angle in the range [0, 2*pi).
    """
    if theta >= 0:
        return theta
    else:
        return 2 * np.pi + theta
    
def normalize_and_symmetric_theta_shift(theta: float) -> float:
    """Normalize an angle to (-pi, pi) and then maps it (0, 2*pi).
    
    Args:
        theta (float): The angle to normalize and shift.
        
    Returns:
        float: The normalized and shifted angle in the range [0, 2*pi).
    """
    return symmetric_theta_shift(get_normalized_angle(theta))

def get_angle_between_deltas(delta_x: float, delta_y: float) -> float:
    """Calculate the angle between two points given their delta coordinates.
    
    Args:
        delta_x (float): The difference in x coordinates.
        delta_y (float): The difference in y coordinates.
        
    Returns:
        float: The angle between the two points in radians.
    """
    return np.atan2(delta_y, delta_x)

def get_angle_between_poses(pose1: Pose2D, pose2: Pose2D) -> float:
    """Calculate the angle between two poses. (pose2 with respect to pose1)
    
    Args:
        pose1 (Pose2D): The first pose.
        pose2 (Pose2D): The second pose.
        
    Returns:
        float: The angle between the two poses in radians.
    """ 
    angle_between_poses = get_angle_between_deltas(pose2.x-pose1.x, pose2.y-pose1.y)

    return get_normalized_angle(angle_between_poses - pose1.theta)

def get_euclidian_distance_between_poses(pose1: Pose2D, pose2: Pose2D) -> float:
    """Calculate the Euclidean distance between two poses.
    
    Args:
        pose1 (Pose2D): The first pose.
        pose2 (Pose2D): The second pose.
        
    Returns:
        float: The Euclidean distance between the two poses.
    """
    return np.sqrt((pose1.x - pose2.x) ** 2 + (pose1.y - pose2.y) ** 2)

def transform_to_matrix(tf: TransformStamped) -> np.ndarray:
    # Extract translation
    t = tf.transform.translation
    x, y, z = t.x, t.y, t.z

    # Extract rotation (quaternion)
    q = tf.transform.rotation
    qx, qy, qz, qw = q.x, q.y, q.z, q.w

    # Convert quaternion to rotation matrix
    R = t3d.quaternions.quat2mat([qw, qx, qy, qz])  # note order: [w, x, y, z]

    # Create homogeneous 4x4 matrix
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = [x, y, z]

    return T