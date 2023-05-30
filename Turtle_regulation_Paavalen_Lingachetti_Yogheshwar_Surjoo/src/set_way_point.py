#!/usr/bin/env python3

import rospy
from std_msgs.msg import Bool
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtle_regulation_paavalen_lingachetti_yogheshwar_surjoo.srv import waypoint as wp
import math

g_turtle_pose = Pose()  # Variable globale pour stocker la pose de la tortue
waypoint = [7, 7]  # Coordonnées du waypoint

def pose_callback(msg):
    global g_turtle_pose
    g_turtle_pose = msg

def calculate_distance(point1, point2):
    x_diff = point2[0] - point1[0]
    y_diff = point2[1] - point1[1]
    distance = math.sqrt(x_diff**2 + y_diff**2)
    return distance

def calculate_angle(point1, point2):
    x_diff = point2[0] - point1[0]
    y_diff = point2[1] - point1[1]
    angle = math.atan2(y_diff, x_diff)
    return angle

def calculate_desired_angle():
    global g_turtle_pose, waypoint
    current_pose = (g_turtle_pose.x, g_turtle_pose.y)
    desired_angle = calculate_angle(current_pose, waypoint)
    return desired_angle

def calculate_linear_error():
    global g_turtle_pose, waypoint
    distance = calculate_distance((g_turtle_pose.x, g_turtle_pose.y), waypoint)
    return distance

def calculate_angular_error(desired_angle):
    global g_turtle_pose
    current_angle = g_turtle_pose.theta
    angular_error = math.atan2(math.sin(desired_angle - current_angle), math.cos(desired_angle - current_angle))
    return angular_error

def calculate_linear_command(error, kp_l):
    command = kp_l * error
    return command

def calculate_angular_command(error, kp_a):
    command = kp_a * error
    return command

def set_waypoint(req):
    global waypoint
    waypoint = [req.x.data, req.y.data]
    return Bool(True)

if __name__ == "__main__":
    
   
    rospy.init_node("set_way_point_node")
    rospy.Service('set_waypoint_service', wp, set_waypoint)
    rate = rospy.Rate(10)

    kp_l = rospy.get_param("~kp_l", 5.0)  # Récupère la valeur de Kp_l du paramètre privé
    kp_a = rospy.get_param("~kp_a", 10.0)  # Récupère la valeur de Kp_a du paramètre privé
    distance_tolerance = rospy.get_param("~distance_tolerance", 0.1)  # Récupère la valeur de distance_tolerance du paramètre privé

    pose_sub = rospy.Subscriber("pose", Pose, pose_callback)
    cmd_pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
    is_moving_pub = rospy.Publisher("is_moving", Bool, queue_size=10)

    while not rospy.is_shutdown():
        desired_angle = calculate_desired_angle()
        linear_error = calculate_linear_error()
        angular_error = calculate_angular_error(desired_angle)

        if linear_error > distance_tolerance:
            linear_command = calculate_linear_command(linear_error, kp_l)
            angular_command = calculate_angular_command(angular_error, kp_a)

            twist_cmd = Twist()
            twist_cmd.linear.x = linear_command
            twist_cmd.angular.z = angular_command
            cmd_pub.publish(twist_cmd)

            is_moving_pub.publish(True)
        else:
            cmd_pub.publish(Twist())
            is_moving_pub.publish(False)

        rate.sleep()
