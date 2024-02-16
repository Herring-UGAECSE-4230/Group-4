import wiringpi

# WiringPi setup for using physical pin numbers
wiringpi.wiringPiSetup()

# Set up square wave output for pin 7 
wiringpi.softToneCreate(7)
wiringpi.softToneWrite(7, 1)

# Empty loop to run square wave 
try:
    while True:
        continue
    
# Reset on keyboard interrupt
except KeyboardInterrupt:
    wiringpi.softToneWrite(7, 0)