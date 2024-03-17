import RPi.GPIO as GPIO
from time import sleep

# GPIO set up for ignoring console warnings and using physical pin numbers
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Set up pin 7 as an output pin
GPIO.setup(5, GPIO.OUT)

# In the while loop, the output is set manually to low or high in certain time intervals
try:
    while True:
        # Changing time interval changes frequency
        GPIO.output(5, GPIO.HIGH)
        sleep(.2)
        GPIO.output(5, GPIO.LOW)
        sleep(.2)

# Reset all pins when program is ended
except KeyboardInterrupt:
    GPIO.cleanup()