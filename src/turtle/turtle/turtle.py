import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class TurtleCircleNode(Node):
    def __init__(self):
        super().__init__('turtle_circle_node')
        # Создаем паблишер для отправки команд скорости в топик /turtle1/cmd_vel
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Таймер срабатывает каждые 0.1 секунды (10 Гц)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 1.0
        
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    turtle_circle_node = TurtleCircleNode()
    
    try:
        rclpy.spin(turtle_circle_node)
    except KeyboardInterrupt:
        pass
    finally:
        turtle_circle_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()