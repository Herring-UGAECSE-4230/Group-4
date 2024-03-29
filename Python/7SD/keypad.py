import RPi.GPIO as GPIO 
GPIO.setmode(GPIO.BCM)
from time import sleep

clear = False

X1 = 18
X2 = 23
X3 = 24
X4 = 25
Y1 = 12
Y2 = 16
Y3 = 20
Y4 = 21

e = 4
d = 17
c = 27
dot = 22
b = 5
a = 6
f = 13
g = 19
invalid = 8
clk1 = 26
clk2 = 7
clk3 = 9
clk4 = 10

clk = [clk1, clk2, clk3, clk4]
dff_pins = [a,b,c,d,e,f,g]
GPIO.setup([X1,X2,X3,X4, dot, invalid], GPIO.OUT)
GPIO.setup([Y1,Y2,Y3,Y4], GPIO.IN)
GPIO.setup(dff_pins, GPIO.OUT)
GPIO.setup([clk1, clk2, clk3, clk4], GPIO.OUT)

def readKeypad(rowNum,char):
    if clear == False:
        curVal = ""
        GPIO.output(rowNum,GPIO.HIGH)
        if GPIO.input(Y1)==1: curVal=char[0]
        if GPIO.input(Y2)==1: curVal=char[1]
        if GPIO.input(Y3)==1: curVal=char[2]
        if GPIO.input(Y4)==1: curVal=char[3]
        GPIO.output(rowNum,GPIO.LOW)
        return curVal
    if clear == True:
        curVal = ""
        GPIO.output(rowNum, GPIO.HIGH)
        if GPIO.input(Y3) == 1:
            curVal = char[2]
        GPIO.output(rowNum,GPIO.LOW)
        return curVal
        

bin_vals = {0:[1,1,1,1,1,1,0], 
            1:[0,1,1,0,0,0,0], 
            2:[1,1,0,1,1,0,1], 
            3:[1,1,1,1,0,0,1], 
            4:[0,1,1,0,0,1,1], 
            5:[1,0,1,1,0,1,1], 
            6:[1,0,1,1,1,1,1], 
            7:[1,1,1,0,0,0,0], 
            8:[1,1,1,1,1,1,1], 
            9:[1,1,1,1,0,1,1],            
            'A':[1,1,1,0,1,1,1], 
            'B':[0,0,1,1,1,1,1], 
            'C':[0,0,0,1,1,0,1], 
            'D':[0,1,1,1,1,0,1], 
            }

def output(gpio_list, states):
    for i in range(len(gpio_list)):
        GPIO.output(gpio_list[i], states[i])
       
def switch(gpio):
    global clear,last, dots
    clear = not clear
    if clear == True:
        last = [GPIO.input(i) for i in dff_pins]
        dots = GPIO.input(dot)
        output(gpio,[0,0,0,0,0,0,0])
        if GPIO.input(dot) == 1:
            GPIO.output(dot,0)
            
    if clear == False:
        output(gpio, last)
        if dots == 1:
            GPIO.output(dot,1)
        if dots == 0:
            GPIO.output(dot,0)
            
def ssd_disp(clk_num, value):
        GPIO.output(invalid, 0)
        try:
            value = int(value)
            output(dff_pins, bin_vals[value])
        except:
            if value == 'A':
                GPIO.output(invalid, 1)
                sleep(0.7)
            if value == 'B':
                GPIO.output(invalid, 1)
                sleep(0.7)
            if value == 'C':
                GPIO.output(invalid, 1)
                sleep(0.7)
            if value == 'D':
                GPIO.output(invalid, 1)
                sleep(0.7)
            if value == '*':
                if GPIO.input(dot) == 0: GPIO.output(dot, 1)
                else: GPIO.output(dot, 0)
            if value == '#':
                switch(dff_pins)
            
        

def latch_value():
    GPIO.output(clk, 1)
    sleep(0.05)
    GPIO.output(clk, 0)



try:
    while True:
        
        if clear == False:
            ssd_disp(clk, readKeypad(X1, [1,2,3,'A']))
            ssd_disp(clk, readKeypad(X2, [4,5,6,'B']))
            ssd_disp(clk, readKeypad(X3, [7,8,9,'C']))
            ssd_disp(clk, readKeypad(X4, ['*',0,'#','D']))
            latch_value()
            sleep(.1)
            
        if clear == True:
            ssd_disp(clk, readKeypad(X4, ['*',0,'#','D']))
            latch_value()
            sleep(.1)
        #switch(dff_pins)
        
except KeyboardInterrupt: 
    GPIO.cleanup()

