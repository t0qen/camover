from gpiozero import PWMOutputDevice, DigitalOutputDevice, PWMLED
import smbus, struct
from picamera2 import Picamera2
import cv2
import time
from threading import Thread
from signal import pause

class Robot:
    def __init__(self):
        # mot init
        self.mot1b = PWMOutputDevice(13, frequency=200)
        self.mot1a = PWMOutputDevice(12, frequency=200)
        self.mot2b = PWMOutputDevice(19, frequency=200)
        self.mot2a = PWMOutputDevice(18, frequency=200)
        self.mot1a.value = 0
        self.mot2b.value = 0
        self.mot1b.value = 0
        self.mot2a.value = 0

        # i2c with xiao
        self.bus = smbus.SMBus(1)
        self.xiao_adress = 0x08
        
        # camera
        self.camera = Picamera2()
        camera_conf = self.camera.create_video_configuration(main={"size": (1280, 720)})
        self.camera.configure(camera_conf)
        self.camera.start()
        self.camera.set_controls({
            "AeEnable": False,
            "ExposureTime": 3000,
            "AnalogueGain": 10.0
        })

        # others
        self.buzzer = PWMOutputDevice(23, frequency=1000)
        self.red_led = PWMLED(24)
    
        self.buzzer_state = False

    def raw_mot(self, m1a, m1b, m2a, m2b):
        self.mot1a.value = m1a
        self.mot1b.value = m1b
        self.mot2a.value = m2a
        self.mot2b.value = m2b

    # def _camera_loop(self):
    #     while self.camera_running:
    #         frame = self.camera.capture_array()
    #         frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    #         frame = cv2.flip(frame, -1)
    #         # skip encode si dernière frame pas consommée
    #         ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
    #         if ret:
    #             self.latest_frame = buffer.tobytes()
    #         time.sleep(0.03)

    def camera_frame(self):
        frame = self.camera.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = cv2.flip(frame, -1)
        return frame

    def set_camera_gain(self, value):
        print(value)
        if value < 50.0 and value > 1.0:
            print(value)
            self.camera.set_controls({"AnalogueGain": float(value)})

    def set_camera_exposure(self, value):
        try:
            print(value)
            self.camera.set_controls({"ExposureTime": int(value)})
        except Exception as e:
            print(f"[robot.py] set_exposure error: {e}")

    def bip(self, state, tone=0.5):
        if state:
            self.buzzer.value = tone
        else: 
            self.buzzer.value = 0

    def set_red_led(self, state, pwm=1.0):
        if state:
            self.red_led.value = pwm
        else: 
            self.red_led.value = 0

    def toggle_buzzer(self, tone=0.9):
        if self.buzzer_state:
            self.buzzer.value = 0
            self.buzzer_state = False
        else:
            self.buzzer.value = tone
            self.buzzer_state = True

    def battery_level(self):
        try:
            raw_data = self.bus.read_i2c_block_data(self.xiao_adress, 0, 4)
            byte_data = bytes(raw_data)
            vin = struct.unpack('<f', byte_data)[0]
            return round(vin, 2)
        except Exception as e:
            print(f"error reading battery level : {e}")
            return None

    def mot(self, direction, pwm=1.0):
        print("[robot.py] direction:", str(direction), ", speed:", str(pwm))
        self.mot1a.value = 0
        self.mot2b.value = 0
        self.mot1b.value = 0
        self.mot2a.value = 0
        if direction == "forward":
            self.mot1a.value = pwm
            self.mot2b.value = pwm
        elif direction == "backward":
            self.mot1b.value = pwm
            self.mot2a.value = pwm
        elif direction == "fast_turn_right":
            self.mot2b.value = pwm
            self.mot1b.value = pwm
        elif direction == "fast_turn_left":
            self.mot1a.value = pwm
            self.mot2a.value = pwm
        elif direction == "turn_left":
            self.mot1a.value = pwm 
            self.mot2b.value = pwm / 3
        elif direction == "turn_right":
            self.mot1a.value = pwm / 3
            self.mot2b.value = pwm
        elif direction == "stop":
            self.mot1a.value = 0 
            self.mot2b.value = 0
            self.mot1b.value = 0
            self.mot2a.value = 0
        else: 
            pass

        