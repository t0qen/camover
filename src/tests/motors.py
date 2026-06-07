from gpiozero import PWMOutputDevice
from signal import pause

motor_1_backward = PWMOutputDevice(12, frequency=200)
motor_1_forward = PWMOutputDevice(13, frequency=200)

motor_2_backward = PWMOutputDevice(18, frequency=200)
motor_2_forward = PWMOutputDevice(19, frequency=200)


motor_1_forward.value = 1
motor_2_forward.value = 1

pause()