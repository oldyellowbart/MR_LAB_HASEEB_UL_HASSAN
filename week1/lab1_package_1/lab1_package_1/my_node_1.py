import rclpy
from rclpy.node import Node
N =0
class SimpleNode(Node):
    def __init__(self):
        super().__init__('lab1_node_test')
        global N
        self.get_logger().info(f'welcome to mobile robotics:{N}')
        N = N+1
        
def main(args=None):
    rclpy.init(args=args)
    node = SimpleNode()
    print("text here")
    # spin_once lets us create the node, log once, and exit cleanly
    rclpy.spin_once(node, timeout_sec=0.1)
    node.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()
