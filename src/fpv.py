from flask import Flask, Response, render_template, request
from signal import pause
from threading import Thread
from ntfy import send_notif

import cv2 
import time
app = Flask(__name__)

def generate_frames(robot):
    while True:
        frame = robot.camera_frame()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


def start_fpv(robot):
    print("** fpv mode selected **")
    send_notif("fpv.py launched", "visit the website to control the robot", "default", "white_check_mark")
    robot.red_led.on()
    print(robot.battery_level())
    @app.route('/video_feed')
    def video_feed():
        return Response(generate_frames(robot), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/control/<direction>')
    def control(direction):
        robot.mot(direction, 1)
        return "[fpv.py] command sent to motor"
    
    @app.route('/battery')
    def battery():
        return str(robot.battery_level())  

    @app.route('/buzzer')
    def buzzer():
        robot.toggle_buzzer()
        return "[fpv.py] command sent to buzzer"
    
    @app.route("/cpu_temp")
    def cpu_temp():
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            temp = int(f.read()) / 1000
        return str(round(temp))
    
    app.run(host='0.0.0.0', port=8080, threaded=True)
    print("[fpv.py] web server launched")
