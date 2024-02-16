#Before running, type 'sudo pigpiod' in the commmand line to initalize pigpio

import pigpio

# Initializing pigpio instance

pi = pigpio.pi()

# Setting up GPIO 4 as a square wave output; pigpio uses the GPIO numbers instead of physical pin numbers
pi.set_PWM_frequency(4, 5)
pi.set_PWM_dutycycle(4, 127.5)

# Empty loop to run square wave
try:
    while True:
        continue

# Reset pin on keyboard interrupt
except KeyboardInterrupt:
    pi.set_PWM_dutycycle(4, 0)
  
    