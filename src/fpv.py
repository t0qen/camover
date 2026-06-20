from flask import Flask, Response, render_template, request
from signal import pause
# from threading import Thread
# import os
import cv2 
import time
app = Flask(__name__)

# def bg_loop(robot):
#     while True:
#         bat_volt = robot.battery_level()

#         if bat_volt < 10.5:
#             print(f"[fpv.py, bg_loop] critical battery level : {bat_volt}")
#             os.system('shutdown -h now')

#         time.sleep(1)

def generate_frames(robot):
    while True:
        frame = robot.camera_frame()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


def start_fpv(robot):
    print("** fpv mode selected **")
    #thread = Thread(target=bg_loop,args=(robot,),daemon=True).start()
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
    
    app.run(host='0.0.0.0', port=8080, threaded=True)
    print("[fpv.py] web server launched")
