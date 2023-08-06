# This example uses two distance sensors to avoid obstacles

from skribot import Skribot
from skribrain import * # pinout definition

robot = Skribot()

robot.set_speed(200)
robot.pick_up() # raise the gripper to not disturb

while True:
    robot.move_forward(500)
    
    left_distance = robot.read_distance_sensor(D1)
    right_distance = robot.read_distance_sensor(D2)
    
    # If any sensor is less than 30 cm from an obstacle, turn left
    if left_distance < 30 or right_distance < 30:
        robot.face_left(700)

