from flask import Flask, Response, render_template, request
from signal import pause
from threading import Thread, Lock
from ntfy import send_notif
import cv2 
import time
from functools import wraps
import secrets

app = Flask(__name__)

current_speed = 1
current_gain = 10.0
current_exposure = 3000

connected_clients = 0
connected_clients_lock = Lock()

def generate_frames(robot):
    global connected_clients
    with connected_clients_lock:
        connected_clients += 1
    try:
        while True:
            frame = robot.camera_frame()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    finally:
        with connected_clients_lock:
            connected_clients -= 1


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != secrets.USERNAME or auth.password != secrets.PASSWORD:
            return Response(
                'Authentification requise', 401,
                {'WWW-Authenticate': 'Basic realm="camover"'}
            )
        return f(*args, **kwargs)
    return decorated


def start_fpv(robot):
    print("** fpv mode selected **")
    send_notif("fpv.py launched", "visit the website to control the robot", "default", "white_check_mark")
    robot.red_led.on()
    print(robot.battery_level())
    @app.route('/video_feed')
    @require_auth
    def video_feed():
        return Response(generate_frames(robot), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    @app.route('/')
    @require_auth
    def index():
        return render_template('index.html')

    @app.route('/control/<direction>')
    @require_auth
    def control(direction):
        robot.mot(direction, current_speed)
        return "[fpv.py] command sent to motor"

    @app.route('/speed/<speed>')
    @require_auth
    def speed(speed):
        global current_speed
        current_speed = float(speed)
        print(f"[fpv.py] global speed : {current_speed}")
        return f"[fpv.py] global speed : {current_speed}"

    @app.route('/gain/<gain>')
    @require_auth
    def gain(gain):
        robot.set_camera_gain(float(gain))
        return "[fpv.py] new gain set"

    @app.route('/exposure/<exposure>')
    @require_auth
    def exposure(exposure):
        robot.set_camera_exposure(float(exposure))
        return "[fpv.py] new exposure set"

    @app.route('/clients')
    @require_auth
    def connected_clients():
        global connected_clients
        return str(connected_clients)

    @app.route('/battery')
    @require_auth
    def battery():
        return str(robot.battery_level())  

    @app.route('/buzzer')
    @require_auth
    def buzzer():
        robot.toggle_buzzer()
        return "[fpv.py] command sent to buzzer"
    
    @app.route("/cpu_temp")
    @require_auth
    def cpu_temp():
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            temp = int(f.read()) / 1000
        return str(round(temp))
    
    app.run(host='0.0.0.0', port=8080, threaded=True)
    print("[fpv.py] web server launched")
