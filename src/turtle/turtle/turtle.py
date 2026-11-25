import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math


class TurtleCircleNode(Node):
    def __init__(self):
        super().__init__('turtle_circle_node')
        # Создаем паблишер для отправки команд скорости в топик /turtle1/cmd_vel
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Таймер срабатывает каждые 0.1 секунды (10 Гц)
        self.x_target=3
        self.y_target=3
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.odom_subscriber = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )
        self.current_odom = None
        
    def odom_callback(self, msg: Odometry):
        self.current_odom = msg
        

    def timer_callback(self):
        if self.current_odom == None:
            return
        x = self.current_odom.pose.pose.position.x
        y = self.current_odom.pose.pose.position.y
        orient_z = self.current_odom.pose.pose.orientation.z
        orient_w = self.current_odom.pose.pose.orientation.w

        yaw = 2 * math.atan2(orient_z, orient_w)

        msg = Twist()
        v = math.sqrt((self.x_target - x)**2 + (self.y_target - y)**2)
        a = math.atan2((self.y_target - y), (self.x_target - x))
        msg.linear.x = 0.0
        error=a-yaw
        if error>math.pi:
            error-=math.pi*2

        if error<-math.pi:
            error+=math.pi*2

        if abs(error)<0.1:

            msg.angular.z = 0.0
            msg.linear.x = v
        else:
            msg.angular.z = error
        
        print(a, yaw, v)
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