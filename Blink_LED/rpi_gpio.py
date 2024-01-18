import RPi.GPIO as GPIO
from time import sleep

# GPIO set up for ignoring console warnings and using physical pin numbers
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Set up pin 7 as an output pin
GPIO.setup(7, GPIO.OUT)

# In the while loop, the output is set manually to low or high in certain time intervals
try:
    while True:
        # Changing time interval changes frequency
        GPIO.output(7, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(7, GPIO.LOW)
        sleep(0.5)

# Reset all pins when program is ended
except KeyboardInterrupt:
    GPIO.cleanup()