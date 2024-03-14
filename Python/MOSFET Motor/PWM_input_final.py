#sudo pigpiod 
import RPi.GPIO as GPIO
from rotary import Rotary #pigpio rotary encoder import
import time

clk = 22
dt = 27
sw = 17

counter = 0
turns = 0 #for turns per second
state = '' #shows either clock wise or ccw 
direction = '' #stores state value 
last = time.time() #used for tps

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

my_rotary = Rotary( #sets up pins from rotary
  clk_gpio=22,
  dt_gpio=27,
  sw_gpio=17
)

my_rotary.setup_rotary( #sets up rotary callbacks, and debounces based on pigpio module
  debounce=200, 
  up_callback=acw, 
  down_callback=cw)

my_rotary.setup_switch(
  debounce=200,
  long_press=True,
  sw_short_callback=sw_short)

while True:
    
    state = ''
    time.sleep(.05)
    
    if state != '':
        turns += 1
        direction = state #stores state for print

    if state == '':
        now = time.time() 
        diff = now - last 
        if diff > 0:
            tps = turns / diff
            print(counter,"Turns per second:", tps, direction) #prints cw or ccw when turning
            direction = '' #all these reset variables
            turns = 0
            last = now
  #deliverable says pulses? counted 20 turns
  