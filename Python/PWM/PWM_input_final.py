#sudo pigpiod 
import RPi.GPIO as GPIO
from time import sleep
from rotary import Rotary #pigpio rotary encoder import

clk = 22
dt = 27
sw = 17

counter = 0
state = ''

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw,GPIO.IN)

lastClk = GPIO.input(clk)
lastdt = GPIO.input(dt)

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

my_rotary.setup_rotary( #sets up rotary callbacks, and automatically debounces
  debounce=200, 
  up_callback=acw, 
  down_callback=cw)

my_rotary.setup_switch(
  debounce=200,
  long_press=True,
  sw_short_callback=sw_short)

while True:
    
    state = ''
    sleep(.2)
    print(counter,state) #prints cw or ccw whenever turning
    
  #deliverable says pulses? counted 20 turns 
  