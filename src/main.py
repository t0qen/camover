from robot import Robot
from fpv import start_fpv
from autonomous import start_autonomous
from threading import Thread
import time
import os

robot = Robot()
autonomous_mode = False

print("| ROBOT CODE LAUNCHED |")
print("")

def main_bg_loop(robot):
    while True:
        bat_volt = robot.battery_level()

        if bat_volt < 10.5:
            print(f"[fpv.py, bg_loop] critical battery level : {bat_volt}")
            os.system('sudo shutdown -h now')

        time.sleep(1)

main_loop = Thread(target=main_bg_loop,args=(robot,),daemon=True)
main_loop.start()

if not autonomous_mode:
    start_fpv(robot)
else: 
    start_autonomous(robot)




