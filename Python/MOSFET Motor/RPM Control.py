#sudo pigpiod 
import RPi.GPIO as GPIO
from rotary import Rotary #pigpio rotary encoder import
from time import sleep
import time

clk = 22
dt = 27
sw = 17

motor = 12
ir = 16
counter = 0
turns = 0 #for turns per second
state = '' #shows either clock wise or ccw 
direction = '' #stores state value 
last = time.time() #used for tps
pressed = 1

rpm_desired = 0


GPIO.setmode(GPIO.BCM)
GPIO.setup(clk,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw,GPIO.IN)
GPIO.setup(ir, GPIO.IN)
GPIO.setup(motor, GPIO.OUT)
   
def cw(self): #clock wise
    global counter, state, rpm_desired
    counter += 1
    state = 'clockwise'
    rpm_desired += 25
    
def acw(self): #clock wise
    global counter, state, rpm_desired
    counter -= 1
    state = 'clockwise'
    rpm_desired -= 25
    if rpm_desired < 0:
        rpm_desired = 0

def sw_short():
    global pressed
    if pressed == 1: pressed = 0
    else: pressed = 1

#sets up pins from rotary
my_rotary = Rotary( clk_gpio=22,dt_gpio=27,sw_gpio=17)

#sets up rotary callbacks, and debounces based on pigpio module
my_rotary.setup_rotary( debounce=200, up_callback=acw, down_callback=cw)
my_rotary.setup_switch(debounce=200,long_press=True,sw_short_callback=sw_short)

pwm = GPIO.PWM(motor, 50)
while True:
    
    #print('IR State: ', GPIO.input(ir))
    if rpm_desired and pressed: 
        pwm.start(50)
    else:
        pwm.stop()
    
#     
#     state = ''
#     time.sleep(.05)
#     print(state)
#     if state != '':
#         turns += 1
#         direction = state #stores state for print
# 
#     if state == '':
#         now = time.time() 
#         diff = now - last 
#         if diff > 0:
#             tps = turns / diff
#             #print(counter,"Turns per second:", tps, direction) #prints cw or ccw when turning
#             direction = '' #all these reset variables
#             turns = 0
#             last = now
  #deliverable says pulses? counted 20 turns
#     print('Pressed: ', pressed)
#     print('RPM: ', rpm_desired)
    #sleep(1)
  