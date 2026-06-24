import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist

from cv_bridge import CvBridge

import cv2
import numpy as np


class CameraFollower(Node):

    def __init__(self):

        super().__init__('camera_follower')

        # SUBSCRIBE TO CAMERA
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        # PUBLISH VELOCITY COMMANDS
        self.publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # CV BRIDGE
        self.bridge = CvBridge()

        # CONTROL PARAMETERS
        self.kp = 0.0001
        self.max_angular_speed = 0.4

        # OBJECT AREA THRESHOLDS
        self.min_area = 500
        self.stop_area = 40000

        # CENTER ALIGNMENT THRESHOLD
        self.center_threshold = 80

        self.get_logger().info("Vision follower node started")

    def image_callback(self, msg):

        # CONVERT ROS IMAGE TO OPENCV IMAGE
        frame = self.bridge.imgmsg_to_cv2(
            msg,
            desired_encoding='bgr8'
        )

        # GET IMAGE DIMENSIONS
        height, width, _ = frame.shape

        # IMAGE CENTER
        image_center_x = width // 2

        # CONVERT TO HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # RED COLOR THRESHOLDS

        # LOWER RED
        #lower_red1 = np.array([20, 100, 100])
        #upper_red1 = np.array([10, 255, 255])

        # UPPER RED
        lower_red2 = np.array([20, 100, 100])
        upper_red2 = np.array([35, 255, 255])

        # CREATE MASKS
        #mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        #mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

        # COMBINE MASKS
        #mask = mask1 + mask2
        mask = cv2.inRange(hsv, lower_red2, upper_red2)

        # REMOVE NOISE
        kernel = np.ones((5, 5), np.uint8)

        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=2)

        # FIND CONTOURS
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        # CREATE TWIST MESSAGE
        twist = Twist()

        # =====================================================
        # OBJECT DETECTED
        # =====================================================

        if len(contours) > 0:

            # LARGEST OBJECT
            largest_contour = max(
                contours,
                key=cv2.contourArea
            )

            area = cv2.contourArea(largest_contour)

            # IGNORE SMALL NOISE
            if area > self.min_area:

                # GET OBJECT MOMENTS
                M = cv2.moments(largest_contour)

                if M["m00"] != 0:

                    # OBJECT CENTER
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    # DRAW OBJECT CENTER
                    cv2.circle(
                        frame,
                        (cx, cy),
                        7,
                        (0, 255, 0),
                        -1
                    )

                    # DRAW IMAGE CENTER LINE
                    cv2.line(
                        frame,
                        (image_center_x, 0),
                        (image_center_x, height),
                        (255, 0, 0),
                        2
                    )

                    # COMPUTE ERROR
                    error = image_center_x - cx

                    # PROPORTIONAL CONTROLLER
                    angular_speed = self.kp * error

                    # LIMIT ROTATION SPEED
                    angular_speed = max(
                        min(angular_speed,
                            self.max_angular_speed),
                        -self.max_angular_speed
                    )

                    # APPLY ROTATION
                    twist.angular.z = angular_speed

                    # =====================================
                    # MOVE FORWARD ONLY IF CENTERED
                    # =====================================

                    if abs(error) < self.center_threshold:

                        # OBJECT FAR
                        if area < self.stop_area:

                            twist.linear.x = 0.10

                        # OBJECT CLOSE
                        else:

                            twist.linear.x = 0.0
                            twist.angular.z = 0.0

                            self.get_logger().info(
                                "Target reached"
                            )

                    else:
                        # ROTATE ONLY
                        twist.linear.x = 0.0

                    self.get_logger().info(
                        f'Error: {error}, '
                        f'Area: {area}, '
                        f'Angular: {angular_speed:.2f}'
                    )

        # =====================================================
        # NO OBJECT DETECTED
        # =====================================================

        else:

            # SEARCH FOR OBJECT
            twist.angular.z = 0.25
            twist.linear.x = 0.0

            self.get_logger().info(
                "Searching for object..."
            )

        # PUBLISH MOTION
        self.publisher.publish(twist)

        # DISPLAY WINDOWS
        cv2.imshow("Camera View", frame)
        cv2.imshow("Mask", mask)

        cv2.waitKey(1)


def main(args=None):

    rclpy.init(args=args)

    node = CameraFollower()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
