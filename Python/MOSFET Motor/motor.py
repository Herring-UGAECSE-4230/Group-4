import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
motor = 19
GPIO.setup(motor, GPIO.OUT)
pwm = GPIO.PWM(motor, 100)

while True:
    try:
        pwm.start(100)
    except KeyboardInterrupt:
        pwm.stop()
        GPIO.cleanup()
# #


