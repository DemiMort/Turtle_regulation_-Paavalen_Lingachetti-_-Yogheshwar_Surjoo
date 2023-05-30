#!/usr/bin/env python3
import rospy
from std_msgs.msg import Bool, Float32
from turtle_regulation_paavalen_lingachetti_yogheshwar_surjoo.srv import waypoint

def send_set_waypoint_request(x, y):
    rospy.wait_for_service('set_waypoint_service')
    try:
        set_waypoint = rospy.ServiceProxy('set_waypoint_service', waypoint)
        response = set_waypoint(Float32(x), Float32(y))
        return response
    except rospy.ServiceException as e:
        print("Service call failed:", str(e))

if __name__ == "__main__":
    rospy.init_node("set_waypoint_client")

    
    for i in range(3):
        
        is_moving = rospy.wait_for_message("is_moving", Bool)
        if not is_moving.data:
           
            x = float(input("Enter the x-coordinate: "))
            y = float(input("Enter the y-coordinate: "))
            response = send_set_waypoint_request(x, y)
            print("Set waypoint successful:", response)
        else:
            print("Turtle is still moving. Cannot send waypoint request.")

        rospy.sleep(1)