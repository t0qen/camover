from flask import Flask, Response
from signal import pause
import cv2 
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
    print(robot.battery_level())
    @app.route('/video_feed')
    def video_feed():
        return Response(generate_frames(robot), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    @app.route('/')
    def index():
        return """
        <html>
            <body>
                <h1>~ camover ~</h1>
                <img src="/video_feed" width="640" height="480">
                <br>
                <p>battery level : <span id="battery-level">loading...</span> V</p>
                <button onclick="sendCommand('forward')">forward</button>
                <button onclick="sendCommand('backward')">backward</button>
                <button onclick="sendCommand('turn_left')">turn left</button>
                <button onclick="sendCommand('turn_right')">turn right</button>
                <button onclick="sendCommand('stop')">stop</button>

                <script>
                function sendCommand(direction) { // send command to motors without reloadingthe page
                    fetch(`/control/${direction}`)
                        .then(response => console.log(response.text()));// log
                }
                setInterval(function() { // refresh battery level every 2s
                    fetch('/battery')
                        .then(response => response.text())
                        .then(level => {
                            document.getElementById('battery-level').textContent = level;
                        });
                }, 2000);
                </script>
            </body>
        </html>
        """

    @app.route('/control/<direction>')
    def control(direction):
        robot.mot(direction, 0.5)
        return "[fpv.py] command sent to motor"
    
    
    @app.route('/battery')
    def battery():
        return str(robot.battery_level())  
        
    
    app.run(host='0.0.0.0', port=8080, threaded=True)
    print("[fpv.py] web server launched")