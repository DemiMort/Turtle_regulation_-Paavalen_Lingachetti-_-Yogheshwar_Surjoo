#!/usr/bin/env python3

import rospy
from turtlesim.msg import Pose
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
import math

g_turtle_pose = Pose()  # Variable globale pour stocker la pose de la tortue
waypoint = {7, 7}  # Coordonnées du waypoint

def pose_callback(msg):
    global g_turtle_pose
    g_turtle_pose = msg

def calculate_desired_angle():
    global g_turtle_pose, waypoint
    x_diff = waypoint[0] - g_turtle_pose.x
    y_diff = waypoint[1] - g_turtle_pose.y
    desired_angle = math.atan2(y_diff, x_diff)
    return desired_angle

def calculate_command(desired_angle, kp):
    error = math.atan2(math.tan(desired_angle - g_turtle_pose.theta), 1)
    command = kp * error
    return command

if __name__ == "__main__":
    rospy.init_node("set_way_point_node")
    rate = rospy.Rate(10)

    kp = rospy.get_param("~kp", 1.0)  # Récupère la valeur de Kp du paramètre privé

    pose_sub = rospy.Subscriber("pose", Pose, pose_callback)
    cmd_pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)

    while not rospy.is_shutdown():
        desired_angle = calculate_desired_angle()
        command = calculate_command(desired_angle, kp)

        twist_cmd = Twist()
        twist_cmd.angular.z = command
        cmd_pub.publish(twist_cmd)

        rate.sleep()
