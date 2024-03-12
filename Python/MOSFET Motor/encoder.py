from rotary import Rotary
import RPi.GPIO as GPIO
from time import sleep

clk = 22
dt = 27
sw = 17

counter = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw,GPIO.OUT)

lastClkState=GPIO.input(clk)

def up_callback():
    counter += 1
    
def down_callback():
    counter -= 1
    
def sw_short():
    counter = 0

def sw_long():
    counter = 1010
    
def rotary_callback():
    print(counter)

my_rotary = Rotary(
  clk_gpio=22,
  dt_gpio=27,
  sw_gpio=17
)

my_rotary.setup_rotary(
  min=0,
  max=9999999999999999999,
  scale=1,
  debounce=200,
  rotary_callback=rotary_callback,
  up_callback=up_callback,
  down_callback=down_callback)

my_rotary.setup_switch(
  debounce=200,
  long_press=True,
  sw_short_callback=sw_short,
  sw_long_callback=sw_long)

while True:
  
  print(counter)
  
  