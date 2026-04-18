import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MultiTurtlePublisher(Node):

    def __init__(self):
        super().__init__('multi_turtle_publisher')

        # Publishers for each turtle
        self.pub1 = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pub2 = self.create_publisher(Twist, '/turtle2/cmd_vel', 10)
        self.pub3 = self.create_publisher(Twist, '/turtle3/cmd_vel', 10)

        self.timer = self.create_timer(0.5, self.timer_callback)
        self.step_square = 0  # step counter for square
        self.step_triangle = 0  # step counter for triangle

    def timer_callback(self):
        # Turtle 1 → Circle
        msg1 = Twist()
        msg1.linear.x = 2.0
        msg1.angular.z = 1.0
        self.pub1.publish(msg1)

        # Turtle 2 → Square
        msg2 = Twist()
        if self.step_square % 8 < 4:
            msg2.linear.x = 2.0
            msg2.angular.z = 0.0
        else:
            msg2.linear.x = 0.0
            msg2.angular.z = 1.57 / 2  # spread turn over 2 ticks
        self.pub2.publish(msg2)
        self.step_square += 1

        # Turtle 3 → Triangle
        msg3 = Twist()
        if self.step_triangle % 6 < 2:
            msg3.linear.x = 2.0
            msg3.angular.z = 0.0
        else:
            msg3.linear.x = 0.0
            msg3.angular.z = 2.094 / 2  # spread turn over 2 ticks
        self.pub3.publish(msg3)
        self.step_triangle += 1


def main(args=None):
    rclpy.init(args=args)
    node = MultiTurtlePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
