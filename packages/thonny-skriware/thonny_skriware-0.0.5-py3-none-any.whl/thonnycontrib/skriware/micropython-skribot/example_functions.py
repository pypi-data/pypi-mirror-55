# This example shows all the functions of the robot
# Uncomment lines to see the effects

from skribot import Skribot

robot = Skribot()

move_time = 500 # milliseconds
speed = 50 # max = 255

# DC Motor
#robot.speed = speed
#robot.move_forward(move_time)
#robot.move_backward(move_time)
#robot.turn_left(move_time)
#robot.turn_right(move_time)
#robot.face_left(move_time)
#robot.face_right(move_time)

# Gripper
#robot.pick_up()
#robot.put_down()
#robot.close_claw()
#robot.open_claw()

# LED
#robot.turn_led_on(255, 255, 0)
#robot.turn_led_on(0, 0, 255, 1)
#robot.turn_led_off()

# Distance sensor
#print('Distance (left):', robot.read_distance_sensor(0), 'cm')
#print('Distance (right):', robot.read_distance_sensor(1), 'cm')

# Line sensor
#print('Line sensor #1 black?', robot.read_line_sensor(0))
#print('Line sensor #2 black?', robot.read_line_sensor(1))
#print('Line sensor #3 black?', robot.read_line_sensor(2))


