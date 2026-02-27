import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseArray,PoseStamped

class GroundTruthFix(Node):
    def __init__(self):
        super().__init__('ground_truth_fix')
        self.robot_name = "tortoisebot"    
        self.sub = self.create_subscription(
            PoseArray,
            '/ground_truth',
            self.callback,
            10)
        self.pub = self.create_publisher(
            PoseArray,
            '/ground_truth_fixed',
            10)

    def callback(self, msg):
        
        if len(msg.poses) == 0:
            return

        pose_msg = PoseStamped()
        pose_msg.header.stamp = self.get_clock().now().to_msg()
        pose_msg.header.frame_id = "odom"   # Must match EKF world_frame

        pose_msg.pose = msg.poses[0]  # <-- adjust if robot not first

        self.pub.publish(pose_msg)
def main():
    rclpy.init()
    node = GroundTruthFix()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()