from robot import Robot
from fpv import start_fpv
from autonomous import start_autonomous
from ntfy import send_notif
from threading import Thread
import time

robot = Robot()
autonomous_mode = False

print("| ROBOT CODE LAUNCHED |")
print("")


if not autonomous_mode:
    fpv = Thread(target=start_fpv,args=(robot,),daemon=True)
    fpv.start()
else: 
    start_autonomous(robot)


while True:
    time.sleep(1)


