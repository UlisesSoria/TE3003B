import puzzlebot.eyes as observation_utils
import cv2
import numpy as np
import os
import rclpy
import tf2_geometry_msgs

from cv_bridge import CvBridge
from geometry_msgs.msg import PointStamped
from puzzlebot_aruco_msgs.msg import ArucoObservation as ArucoMsg
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import CompressedImage, Image
from tf2_ros import Buffer, TransformListener


class PuzzlebotAruco(Node):
    def __init__(self):
        super().__init__('puzzlebot_aruco_node')

        self.ros_distro = os.getenv("ROS_DISTRO").strip()
        self.namespace = self.get_namespace().strip('/')

        # Declare and get parameters
        self.declare_parameter('aruco_side_length', 0.15)
        self.declare_parameter('camera_matrix', [0.]*9)
        self.declare_parameter('camera_distortion', [0.]*5)
        self.declare_parameter('camera_optical_frame', 'camera_link_optical')

        self.aruco_side_length = self.get_parameter('aruco_side_length').get_parameter_value().double_value
        self.camera_matrix = np.array(self.get_parameter('camera_matrix').get_parameter_value().double_array_value).reshape((3, 3))
        self.dist_coeffs = np.array(self.get_parameter('camera_distortion').get_parameter_value().double_array_value).reshape((5, 1))
        self.camera_optical_frame = self.get_parameter('camera_optical_frame').get_parameter_value().string_value

        # Subscribers
        self.create_subscription(CompressedImage, 'camera/compressed', self.camera_callback, qos_profile_sensor_data)

        # Publishers
        self.aruco_image_publisher = self.create_publisher(Image, 'aruco_image', qos_profile_sensor_data)
        self.aruco_observation_publisher = self.create_publisher(ArucoMsg, 'aruco_observation', qos_profile_sensor_data)

        # TF
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.bridge = CvBridge()
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.parameters = cv2.aruco.DetectorParameters()
        if self.ros_distro == 'jazzy':
            self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.parameters)

        self.get_logger().info("Puzzlebot Aruco Node has started")

    def camera_callback(self, msg):
        # Decompress image
        np_arr = np.frombuffer(msg.data, np.uint8)
        cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        if self.ros_distro == 'humble':
            corners, ids, _ = cv2.aruco.detectMarkers(gray_image, self.aruco_dict, parameters=self.parameters)
        elif self.ros_distro == 'jazzy':
            corners, ids, _ = self.detector.detectMarkers(gray_image)

        ids = ids.flatten() if ids is not None else []

        if len(corners) > 0:
            for corner, aruco_id in zip(corners, ids):
                rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corner, self.aruco_side_length, self.camera_matrix, self.dist_coeffs)
                cv2.drawFrameAxes(cv_image, self.camera_matrix, self.dist_coeffs, rvec[0][0], tvec[0][0], 0.05)

                # Draw marker
                pts = corner.reshape((4, 2)).astype(int)
                for i in range(4):
                    cv2.line(cv_image, tuple(pts[i]), tuple(pts[(i+1)%4]), (0, 255, 0), 2)
                cv2.putText(cv_image, str(aruco_id), (pts[3][0], pts[3][1] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                marker_point = PointStamped()
                marker_point.header.stamp = self.get_clock().now().to_msg()
                marker_point.header.frame_id = self.camera_optical_frame.lstrip('/')
                marker_point.point.x = tvec[0][0][0]
                marker_point.point.y = tvec[0][0][1]
                marker_point.point.z = tvec[0][0][2]

                try:
                    transformed_point = self.tf_buffer.transform(
                        marker_point,
                        'base_footprint',
                        timeout=rclpy.duration.Duration(seconds=1.0)
                    )

                    distance, angle = observation_utils.observate_from_deltas(
                        transformed_point.point.x, transformed_point.point.y, 0.0
                    )

                    # Annotate values
                    cv2.putText(cv_image, f"{distance:.2f} m", (pts[1][0]+7, pts[1][1]+12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    cv2.putText(cv_image, f"{angle:.2f} rad", (pts[1][0]+7, pts[1][1]+27), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    msg_obs = ArucoMsg()
                    msg_obs.id = int(aruco_id)
                    msg_obs.distance = distance
                    msg_obs.angle = angle
                    self.get_logger().info(f"Detected Aruco ID: {aruco_id}, Distance: {distance:.2f} m, Angle: {angle:.2f} rad")
                    self.aruco_observation_publisher.publish(msg_obs)

                except Exception as e:
                    self.get_logger().warn(f"TF transform failed: {e}")

        # Publish annotated image
        image_msg = self.bridge.cv2_to_imgmsg(cv_image, encoding='bgr8')
        image_msg.header = msg.header
        self.aruco_image_publisher.publish(image_msg)


def main():
    rclpy.init()
    node = PuzzlebotAruco()
    try:
        rclpy.spin(node)
    except Exception as e:
        node.get_logger().error(f"Exception: {e}")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
