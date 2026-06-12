from flask import Flask
from signal import pause

app = Flask(__name__)


# def generate_frames():
    # while True:
        # frame = robot.get_camera_frame()
        # ret, buffer = cv2.imencode('.jpg', frame)
        # frame_bytes = buffer.tobytes()
        # yield (b'--frame\r\n'
            #    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')



def start_fpv(robot):
    print("** fpv mode selected **")

    @app.route('/video_feed')
    def video_feed():
        pass
        # return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    @app.route('/')
    def index():
        return """
        <html>
            <body>
                <h1>Flux vidéo du robot</h1>
                <img src="/video_feed" width="640" height="480">
                <br>
                <a href="/control/forward">Avancer</a>
                <a href="/control/backward">Reculer</a>
                <a href="/control/left">Gauche</a>
                <a href="/control/right">Droite</a>
                <a href="/control/stop">Stop</a>
            </body>
        </html>
        """

    @app.route('/control/<direction>')
    def control(direction):
        robot.mot(direction, 0.5)
        
    
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=True)
    print("[fpv.py] web server launched")