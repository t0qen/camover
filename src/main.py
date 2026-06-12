from robot import Robot
from fpv import start_fpv
from autonomous import start_autonomous

robot = Robot()
autonomous_mode = False

print("| ROBOT CODE LAUNCHED |")
print("")

if not autonomous_mode:
    start_fpv(robot)
else: 
    start_autonomous(robot)




