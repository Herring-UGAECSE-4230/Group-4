import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
motor = 12
ir = 16
GPIO.setup(motor, GPIO.OUT)
GPIO.setup(ir, GPIO.IN)
pwm = GPIO.PWM(motor, 20)


try:
    while True:
        print("IR State: ", GPIO.input(ir))
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
# #


