#sudo pigpiod 
import RPi.GPIO as GPIO
from rotary import Rotary #pigpio rotary encoder import does most of work
import time

clk = 22
dt = 27
sw = 17

counter = 0
stored = 0

#for turns per second
state = '' #displays clockwise or ccw
direction = '' #used to store state

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw,GPIO.IN)

def acw(self): #anti clock wise
    global counter, state
    counter += 1
    state = 'counter clockwise'
    
def cw(self): #clock wise
    global counter, state
    counter -= 1
    state = 'clockwise'

def sw_short():
    print("press")
    time.sleep(.5)

#sets up pins from rotary
my_rotary = Rotary( clk_gpio=22,dt_gpio=27,sw_gpio=17)

#sets up rotary callbacks, and automatically debounces
my_rotary.setup_rotary(debounce=200, up_callback=acw,  down_callback=cw)

my_rotary.setup_switch(debounce=200,long_press=True,sw_short_callback=sw_short)

while True:
    
    time.sleep(.1)

    if stored != counter:
        now = time.time()
        denom = now - start
        tps = 2 / denom
        print("Turns per second:", tps)

    if state != '':
        start = time.time()
        stored = counter
      
    print(state,counter)
