#!/usr/bin/bash
rsync -av --delete * pi@192.168.1.37:/home/pi/camover
ssh pi@192.168.1.37 "python3 /home/pi/camover/main.py"
