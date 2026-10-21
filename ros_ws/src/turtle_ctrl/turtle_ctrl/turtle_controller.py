import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
import numpy as np
from geometry_msgs.msg import Twist
from rcl_interfaces.msg import Parameter, SetParametersResult

class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')

        self.get_logger().info('Turtle Controller Node has been started')
        self.get_logger().info('Subscribed to turtle pose')
        self.post_subscription = self.create_subscription(
            Pose, 'turtle1/pose', self.pose_callback, 1
        )
        self.cmd_vel_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 1)

        self.goal_pose = np.array([10.0,9.0])
        self.current_pose = None
        self.kp = self.declare_parameter('kp', 1.0).get_parameter_value().double_value
        self.add_on_set_parameters_callback(self.parameter_callback)
        self.timer_period = 0.1
        self.timer = self.create_timer(self.timer_period, self.timer_callback)


    def parameter_callback(self, params: list[Parameter]):
        for param in params:
            if param.name == 'kp':
                self.kp = param.value  
                self.get_logger().info(f"updated kp to: {self.kp}")
                return SetParametersResult(successful=True)
        return SetParametersResult(successful=False, reason="Invalid parameter type or name.")

    
    def pose_callback(self, msg: Pose):
        # self.get_logger().info(f"Turtle Pose: x={msg.x}, y={msg.y}, theata={msg.theta}")
        self.current_pose = np.array([msg.x, msg.y])
        
        

    def timer_callback(self):
        self.get_logger().info("Timer Callback executed.")
        if self.current_pose is not None:
            error = self.goal_pose - self.current_pose
            velocity = self.kp * error
            cmd_vel_msg = Twist()
            cmd_vel_msg.linear.x = velocity[0]
            cmd_vel_msg.linear.y = velocity[1]
            self.cmd_vel_publisher.publish(cmd_vel_msg)


def main():
    rclpy.init()
    turtle_controller = TurtleController()
    rclpy.spin(turtle_controller)
    turtle_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()