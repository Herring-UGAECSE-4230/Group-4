#sudo pigpiod 
import RPi.GPIO as GPIO
from rotary import Rotary #pigpio rotary encoder import does most of work
import time

clk = 22
dt = 27
sw = 17

counter = 0
higher = 0
lower = 0

#for turns per second
state = '' #displays clockwise or ccw
direction = '' #used to store state

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
    time.sleep(.5)
    
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
    
    higher = counter + 2
    lower = counter - 2
    
    print(higher, lower)
    
    while counter != higher and counter != lower: 
        state = ''
        if state != '':
            start = time.time()  
        print(counter, state)
        time.sleep(.1)
        
    now = time.time()
    diff = now - start
    print(diff)
#     
#     if state == '':
#         now = time.time() #gets time difference for just one turn
#         diff = now - last #difference
#         if diff > 0:
#             tps = turns / diff
#             print(counter, "Turns per second:", tps, direction)
#             turns = 0
#             last = now
#             direction = '' #clears so only shows direction while turning
#             
    
#deliverable says pulses? counted 20 turns for a full loop of the encoder
  