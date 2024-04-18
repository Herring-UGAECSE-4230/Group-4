#sudo pigpiod 
import RPi.GPIO as GPIO
from rotary import Rotary #pigpio rotary encoder import
from time import sleep
import time
from read_RPM import reader
import pigpio

pi = pigpio.pi() #initializes pigpio

clk = 22 #encoder pins
dt = 27
sw = 17

ir = 16 #ir sensor pin
motor = 12
counter = 0 #counts falling edge from fan
pressed = 1 #bool for on / off of fan

rpm_desired = 0 
duty = 0 #duty cycle 

GPIO.setmode(GPIO.BCM)
GPIO.setup([clk,dt,sw], GPIO.IN)
GPIO.setup(ir, GPIO.IN)
GPIO.setup(motor, GPIO.OUT)
 
pwm = GPIO.PWM(motor, 10000)

def cw(self): #turning clock wise in the encoder
    global rpm_desired, duty, pressed
    rpm_desired += 250 #expected value
    if rpm_desired > 0:
        if duty <= 95: #changes duty cycle since frequency does not affect it
            duty += 5
        pwm.start(duty) #starts at new duty cycle
        pressed = 1
    if rpm_desired > 5000: 
        rpm_desired = 5000 #max rpm value 
    
def acw(self): #counter clock wise very similar to other function
    global rpm_desired, duty, pressed
    rpm_desired -= 250
    if duty >= 5: #limits duty cycle from being negative
        duty -= 5 
    pwm.start(duty)
    pressed = 1 #ensures pressed state is correct with motor
    if rpm_desired <= 0:
        pwm.stop()
        pressed = 0 #likewise to line 48
        rpm_desired = 0
   
def switch(): #switch function for encoder
    global pressed, duty 
    if pressed == 1: #if running stops running
        pwm.stop()
        pressed = 0
    
    else: #if NOT running then starts running
        pwm.start(duty)
        pressed = 1
    print("Pressed: ", pressed)
    
#sets up pins from rotary
my_rotary = Rotary(clk_gpio=22,dt_gpio=27,sw_gpio=17) 

#sets up rotary callbacks, and debounces based on pigpio Rotary class
my_rotary.setup_rotary(debounce=200, up_callback=acw, down_callback=cw)
my_rotary.setup_switch(debounce=200,long_press=False,sw_short_callback=switch)

#finds the RPM from the read_RPM pigpio file, does heavy lifting since none of our methods were accurate
rotations = reader(pi, gpio = ir, pulses_per_rev = 3)

try:
    
    if rpm_desired > 0 and pressed == 1:
        print("bruhruhruh")
        pwm.start(duty)
    
    else:
        pwm.stop()
        
    while True:
        speed = rotations.RPM()
        print(" Set RPM:", rpm_desired, "\n","Actual RPM:", speed)
        sleep(.5)
    
except:
    pwm.stop()
    GPIO.cleanup()
