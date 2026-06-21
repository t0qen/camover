from robot import Robot
from ntfy import send_notif
import os
import time 

robot = Robot()
while True:
    bat_volt = robot.battery_level()

    if bat_volt < 11.5 and bat_volt > 11:
        print(f"[power-management.py] warning battery level : {bat_volt}")
        send_notif("power warning", "battery level is low", "high", "warning")
        robot.red_led.blink()
    elif bat_volt < 11 and bat_volt > 10.75:
        print(f"[power-management.py] critical battery level : {bat_volt}")
        send_notif("SUPER LOW POWER", "battery level is very low and it gotta shutdown", "urgent", "no_entry_sign")
        robot.red_led.blink(0.5, 0.5)
    elif bat_volt < 10.75:
        print(f"[power-management.py] shutdown due to critical battery level : {bat_volt}")
        send_notif("camover shutdown", "the battery is too low", "urgent", "no_entry_sign")
        time.sleep(5)
        os.system('sudo shutdown -h now')

    else:
        pass

    time.sleep(5)
