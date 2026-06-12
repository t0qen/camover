from gpiozero import PWMLED
from signal import pause

buzzer = PWMLED(23)
buzzer.value = 0.9
pause()