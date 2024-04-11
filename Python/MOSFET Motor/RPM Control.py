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
duty = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk,GPIO.IN)
GPIO.setup(dt,GPIO.IN)
GPIO.setup(sw,GPIO.IN)
GPIO.setup(ir, GPIO.IN)
GPIO.setup(motor, GPIO.OUT)
   
def cw(self): #clock wise
    global counter, state, rpm_desired, duty
    counter += 1
    state = 'clockwise'
    rpm_desired += 25
    if rpm_desired > 0:
        if duty <= 95: duty += 5
        pwm.start(duty)
    
    print('RPM: ', rpm_desired)
    
def acw(self): #clock wise
    global counter, state, rpm_desired, duty
    counter -= 1
    state = 'clockwise'
    rpm_desired -= 25
    if duty >= 5: duty -= 5
    pwm.start(duty)
    if rpm_desired <= 0:
        pwm.stop()
        rpm_desired = 0
    print('RPM: ', rpm_desired, duty)
def increment(self):
    global counter 
    counter += 1


GPIO.add_event_detect(ir, GPIO.FALLING, callback=increment, bouncetime= 10)

def sw_short():
    global pressed, duty
    if pressed == 1:
        pressed = 0
        pwm.stop()
    
    else:
        pressed = 1
        pwm.start(duty)
    print("Pressed: ", pressed)
    

#sets up pins from rotary
my_rotary = Rotary( clk_gpio=22,dt_gpio=27,sw_gpio=17)

#sets up rotary callbacks, and debounces based on pigpio module
my_rotary.setup_rotary( debounce=200, up_callback=acw, down_callback=cw)
my_rotary.setup_switch(debounce=200,long_press=True,sw_short_callback=sw_short)

pwm = GPIO.PWM(motor, 1)

try:
    if rpm_desired > 0 and pressed == 1:
        pwm.start(duty)
            
    else:
        pwm.stop()
        print("stop")
    while True:
        
        pass
        
except:
    pwm.stop()
    GPIO.cleanup()
    #sleep(1)
    
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
  