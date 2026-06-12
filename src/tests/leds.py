from gpiozero import PWMLED
from signal import pause

led = PWMLED(24)
led.value = 0.1
pause()