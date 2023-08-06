# This example uses two line distance sensors of the robot
# to follow a black line

from skribot import Skribot
from skribrain import * # pinout definition

robot = Skribot()

robot.set_speed(76)

while True:
    left_black = robot.read_line_sensor(LINE1)
    right_black = robot.read_line_sensor(LINE3)

    if (not left_black and not right_black) or (left_black and right_black):
        robot.move_forward(25)
    else:
        if left_black:
            robot.face_right(25)
        elif right_black:
            robot.face_left(25)
            
