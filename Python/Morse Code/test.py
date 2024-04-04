import RPi.GPIO as GPIO
from time import sleep
spk = 6
GPIO.setmode(GPIO.BCM)
GPIO.setup(spk, GPIO.OUT)
pwm = GPIO.PWM(spk, 1000)
try:
    pwm.start(50)
    while True:
        pass
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()