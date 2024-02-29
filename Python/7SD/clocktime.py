import RPi.GPIO as GPIO 
GPIO.setmode(GPIO.BCM)
from time import sleep
from datetime import datetime
from time import perf_counter

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

clk1 = 10
clk2 = 9
clk3 = 7
clk4 = 26
clk5 = 11

counter = 0
number = 0
bcount = 0
key1 = 0
key2 = 0
key3 = 0
key4 = 0
h2 = 0
delays = 0
conc = 0 # concatenated number
concatenated = False
value1 = []
value2 = []
value3 = []
value4 = []
last1 = []
last2 = []
last3 = []
last4 = []
clear = False
auto_time = False
manual_time = False
toggle = False
free_mode = True
clock = [clk1,clk2,clk3,clk4]
dff_pins = [a,b,c,d,e,f,g]
values = [value1,value2,value3,value4]

GPIO.setup([X1,X2,X3,X4, dot, invalid], GPIO.OUT)
GPIO.setup([Y1,Y2,Y3,Y4], GPIO.IN)
GPIO.setup(dff_pins, GPIO.OUT)
GPIO.setup([clk1,clk2,clk3, clk4,clk5], GPIO.OUT)

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
       
def switch(clk_num, gpio):
    global clear,last, dots
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
    latch_value(clk_num)       
def ssd_disp(clk_num, value):
    global clock, setssd, counter, last, bcount
    global clear, dots, auto_time, toggle, free_mode, manual_time
    try:
        
        value = int(value)
        output(dff_pins, bin_vals[value])
        GPIO.output(invalid, 0)
        counter += 1
        
    except:
        if value == 'A':
            GPIO.output(invalid, 1)
            if counter >= 4:
                auto_time = True
                free_mode = False
                manual_time = False
                print("fnally here")
        if value == 'B':
            GPIO.output(invalid, 1)
            sleep(.1)
            GPIO.output(invalid, 0)
            bcount += 1
            if bcount == 1:
                last = [GPIO.input(i) for i in dff_pins]
                dots = GPIO.input(dot)
                auto_time = False
                free_mode = False
                manualset()
            if bcount == 3:
                auto_time = False
                manual_time = False
                free_mode = True
                counter = -5 
                bcount = 0
                for x in range(4): 
                    ssd_disp(clock[x], 0)
                print("bcount3")
                
        if value == 'C':
            GPIO.output(invalid, 1)
            
        if value == 'D':
            GPIO.output(invalid, 1)
            
        if value == '*':
            if GPIO.input(dot) == 0: GPIO.output(dot, 1)
            else: GPIO.output(dot, 0)
        if value == '#':
            GPIO.output(invalid, 1)
            sleep(.5)
            GPIO.output(invalid, 0)
            clear = not clear
            if auto_time == True:
                for x in range(4):
                    switch(clock[x], dff_pins)
            toggle = not toggle
            
    latch_value(clk_num)
     
def latch_value(clk_num):
    GPIO.output(clk_num, 1)
    sleep(0.05)
    GPIO.output(clk_num, 0)
    sleep(0.05)

def ssdLoop(clk_num):
    global counter
    if clear == False:
        ssd_disp(clk_num, readKeypad(X1, [1,2,3,'A']))
        ssd_disp(clk_num, readKeypad(X2, [4,5,6,'B']))
        ssd_disp(clk_num, readKeypad(X3, [7,8,9,'C']))
        ssd_disp(clk_num, readKeypad(X4, ['*',0,'#','D']))
        sleep(.1)
    if clear == True:
        ssd_disp(clk_num, readKeypad(X4, ['*',0,'#','D']))
        sleep(.1)
        
def getTime(now=None):
    global pm
    if now is None:
        now = datetime.now()
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    pm = False
    if hour > 12:
        pm = True
        hour = hour - 12
        
    hour = '{0:02d}'.format(hour)
    minute = '{0:02d}'.format(minute)

    ssd_h1 = int(hour[0])
    ssd_h2 = int(hour[1])
    ssd_m1 = int(minute[0])
    ssd_m2 = int(minute[1])
    return [ssd_h1, ssd_h2, ssd_m1, ssd_m2, pm]

def auto():
    current_time = datetime.now()
    curr = getTime(current_time)
    ssd_disp(clk1, curr[0])
    ssd_disp(clk2, curr[1])
    ssd_disp(clk3, curr[2])
    ssd_disp(clk4, curr[3])
    if curr[4] == True:
        GPIO.output(dot, 1)
    
def manualset():
    global counter, clock, toggle, clear , manual_time, key1, h2, concatenated, last1,last2, delays, keys 
    global key2, key3, key4
    counter = 0
    while counter < 4 and counter >= 0:
        clear = not clear
        switch(clock[counter], dff_pins) #this makes each SSD flash until a value is input
        if counter == 0:
            ssdLoop(clk1)
            sleep(.1)
            last1 = [GPIO.input(i) for i in dff_pins]
            keyfinderHH(last1)
            if key1 == 2:
              h2 = 2          
        if counter == 1:
            ssdLoop(clk2)
            sleep(.1)
            last2 = [GPIO.input(i) for i in dff_pins]
            keyfinderH2(last2)
            if concatenated == False:
                manual_get_time()
        if counter == 2:
            ssdLoop(clk3)
            sleep(.1)
            last3 = [GPIO.input(i) for i in dff_pins]
            keyfinderMM(last3)
        if counter == 3:
            ssdLoop(clk4)
            sleep(.1)
            last4 = [GPIO.input(i) for i in dff_pins]
            keyfinderM2(last4)
            manual_time = True
    while manual_time == True:
        
        last4 = bin_vals[key4]
        last3 = bin_vals[key3]
        last2 = bin_vals[key2]
        last1 = bin_vals[key1]
        last_dff = [last1,last2,last3,last4]
        if toggle == False:
            for x in range(4):
                output(dff_pins, last_dff[x])
                ssdLoop(clock[x])
        if toggle == True:
            for x in range(4):
                output(dff_pins, [0,0,0,0,0,0,0,0])
                ssdLoop(clock[x])
        ssdLoop(clk5)
        counter = 5
        delays += 1
        if delays == 3:
            delay()
            delays = 0
def manual_get_time():
    global key1, key2, last1,last2, concatenated, dot
    conc = str(key1) + str(key2)
    conc = int(conc)
    if conc > 12:
        conc = conc - 12
        GPIO.output(dot, 1)
    if conc < 10:
            key1 = 0
            key2 = conc
    if conc >= 10:
        key1 = str(conc)[0]
        key2 = str(conc)[1]
        key1 = int(key1)
        key2 = int(key2)
    last1 = bin_vals[key1]
    last2 = bin_vals[key2]
    concatenated = True


def delay():
    global key1,key2,key3,key4, last1,last2,last3,last4, keys
    
    key4 +=1
    if key4 > 9:
        key4 = 0
        key3 += 1
        if key3 > 5:
            key3 = 0
            key2 += 1
            if key2 > (9 if key1 == 0 else 2):
                key2 = 0 if key1 == 0 else 1
                key1 ^= 1
    ssd_disp(clk1, key1)
    ssd_disp(clk2, key2)
    ssd_disp(clk3, key3)
    ssd_disp(clk4, key4)
    sleep(2)
def keyfinderHH(values):
    global key1, counter, invalid, value1
    for key, value in bin_vals.items():
        if value == values:
            key1 = key
            value1 = value
    if key1 > 2:
        GPIO.output(invalid, 1)
        counter = 0
        
def keyfinderH2(values):
    global key2, counter, invalid, h2, value2
    for key, value in bin_vals.items():
        if value == values:
            key2 = key
            value2 = value
    if h2 == 2:
        if key2 > 4:
            GPIO.output(invalid, 1)
            counter = 1
            
def keyfinderMM(values):
    global key3, two, counter, value3
    for key, value in bin_vals.items():
        if value == values:
            key3 = key
            value3 = value
    if key3 > 5:
        GPIO.output(invalid, 1)
        counter = 2

def keyfinderM2(values):
    global key4
    for key, value in bin_vals.items():
        if value == values:
            key4 = key
            
    

current_time = datetime.now()
curr = getTime(current_time)


counter = 100

try:
    while True:
        
        output(dff_pins, [1,1,1,1,1,1,0,0])
        GPIO.output(dot,0)
        while free_mode == True:
            ssdLoop(clk1)
            ssdLoop(clk2)
            ssdLoop(clk3)
            ssdLoop(clk4)
            counter = 100
        while auto_time == True:
            ssdLoop(clk5)
            if clear == False:
                auto()

except KeyboardInterrupt: 
    GPIO.cleanup()

