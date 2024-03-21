import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
motor = 12
ir = 13
GPIO.setup(motor, GPIO.OUT)
pwm = GPIO.PWM(motor, 500)


try:
    pwm.start(50)
    while True:
        pass
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
# #


