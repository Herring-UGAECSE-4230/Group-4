#sudo pigpiod 
import RPi.GPIO as GPIO
from rotary import Rotary #pigpio rotary encoder import
from time import sleep
import time

clk = 22
dt = 27
sw = 17

ir = 16
motor = 12
counter = 0
pressed = 1

rpm_desired = 0
duty = 0
state = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup([clk,dt,sw], GPIO.IN)
GPIO.setup(ir, GPIO.IN)
GPIO.setup(motor, GPIO.OUT)
 
pwm = GPIO.PWM(motor, 1)

def cw(self): #clock wise
    global counter, state, rpm_desired, duty, pressed
    rpm_desired += 25
    if rpm_desired > 0:
        if duty <= 95:
            duty += 5
        pwm.start(duty)
        pressed = 1
    if rpm_desired > 500:
        rpm_desired = 500
    print('Expected RPM: ', rpm_desired, duty)
    
def acw(self): #clock wise
    global state, rpm_desired, duty, pressed
    rpm_desired -= 25
    if duty >= 5:
        duty -= 5
    pwm.start(duty)
    pressed = 1
    if rpm_desired <= 0:
        pwm.stop()
        pressed = 0
        rpm_desired = 0
    print('Expected RPM: ', rpm_desired, duty)
   
def switch():
    global pressed, duty
    if pressed == 1:
        pwm.stop()
        pressed = 0
    
    else:
        pwm.start(duty)
        pressed = 1
    print("Pressed: ", pressed)

def increment(self):
    global counter, state
    if not GPIO.input(ir) and state:
        counter += 1
        state = 0
    else: state = 1
    
def rotation():
    global counter
    counter = 0
    start = time.time()
    spinning = True
    while spinning:
        #print(counter)
        if time.time() - start >= 1:
            diff = time.time() - start
            rpm = (counter / diff ) * 60
            print("RPM:", rpm, counter)
            counter = 0
            spinning = False
    
    
#sets up pins from rotary
my_rotary = Rotary(clk_gpio=22,dt_gpio=27,sw_gpio=17)

#sets up rotary callbacks, and debounces based on pigpio module
my_rotary.setup_rotary(debounce=200, up_callback=acw, down_callback=cw)
my_rotary.setup_switch(debounce=200,long_press=False,sw_short_callback=switch)

GPIO.add_event_detect(ir, GPIO.FALLING, callback=increment, bouncetime = 30)

try:
    if rpm_desired > 0 and pressed == 1:
        pwm.start(duty)
    
    else:
        pwm.stop()
        
    while True:
        
        #rotation()
        print(counter, GPIO.input(ir))
        sleep(.5)
except:
    pwm.stop()
    GPIO.cleanup()


# 
# def increment(self):
#     global counter, state 
#     if not GPIO.input(ir) and state:
#         counter += 1
#         state = 0
#     else: state = 1
# 
# last = time.time()
# 
# def pulse(self):
#     global counter, last
#     counter += 1
#     curr = time.time()
#     diff = curr - last
#     last = curr
#     
#     if counter == 3:
#         rpm = 60 / (3 * diff)
#         print('Actual RPM: ', rpm)
#         
#         counter = 0
#     
# def calc():
#     global counter
#     
#     start = time.time()
#     while time.time() - start < 60:
#         #print(counter, GPIO.input(ir))
#         pass
#     print('Actual RPM: ', counter / 3)
#     counter = 0