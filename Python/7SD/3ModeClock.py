import RPi.GPIO as GPIO 
GPIO.setmode(GPIO.BCM)
import time
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
clk5 = 11 #imaginary clk that is used to switch value with out changing visible clocks, love this

counter = 0 #used to move around the functions in the program
number = 0
bcount = 0 #This is for the 3 b's
key1 = 0 #These store the value being displayed in the manual set
key2 = 0
key3 = 0
key4 = 0
h2 = 0
delays = 0 #used to manually count to a minute in a while loop
conc = 0 # concatenated number used to check if HH > 12
time_num = 0 #timer number

concatenated = False #This is used so that the HH checker only goes once
clear = False #For # button in the automatic time set
auto_time = False 
manual_time = False
toggle = False #For the # button in the manual time set
free_mode = True #00:00 after the 3 b's
timer = False

last1 = [] #These are the binary values for a given number, used for storing 
last2 = []
last3 = []
last4 = []

clock = [clk1,clk2,clk3,clk4]
dff_pins = [a,b,c,d,e,f,g] #pins of flip flop


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
    if clear == True: #only reads # column after pressing # button
        curVal = ""
        GPIO.output(rowNum, GPIO.HIGH)
        if GPIO.input(Y3) == 1:
            curVal = char[2]
        GPIO.output(rowNum,GPIO.LOW)
        return curVal
        

bin_vals = {0:[1,1,1,1,1,1,0],  #flip flop pin state for each number
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
        GPIO.output(gpio_list[i], states[i]) #makes outputing each pin way easier 
       
def switch(clk_num, gpio):
    global clear,last, dots
    if clear == True:
        last = [GPIO.input(i) for i in dff_pins] #if pressed, it stores the value and then changes the output to zero
        dots = GPIO.input(dot) #store dot value
        output(gpio,[0,0,0,0,0,0,0])
        if GPIO.input(dot) == 1:
            GPIO.output(dot,0)
        
    if clear == False:
        output(gpio, last) #calls stored last value from up above
        if dots == 1:
            GPIO.output(dot,1)
        if dots == 0:
            GPIO.output(dot,0)
    latch_value(clk_num)       
def ssd_disp(clk_num, value): #This sets the value of the ssd display based on what you input
    global clock, setssd, counter, last, bcount, last1,last2,last3,last4,last_dff
    global clear, dots, auto_time, toggle, free_mode, manual_time, timer
    try:
        
        value = int(value)
        output(dff_pins, bin_vals[value]) 
        GPIO.output(invalid, 0)
        counter += 1
        
    except:
        if value == 'A':
            GPIO.output(invalid, 1)
            if counter >= 4:
                timer = False
                free_mode = False
                manual_time = False
                auto_time = True #This is the automatic mode, setting everything else false
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
                timer = False
                manual_time = False
                manualset()
            if bcount == 3:
                timer = False
                auto_time = False
                manual_time = False
                free_mode = True
                counter = -5 
                bcount = 0
                for x in range(4): 
                    ssd_disp(clock[x], 0) #sets all clocks to zero
                print("bcount3")
                
        if value == 'C':
            GPIO.output(invalid, 1)
            timer = True
            manual_set()
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
     
def latch_value(clk_num): #this sens the signal to the corresponding clock
    GPIO.output(clk_num, 1)
    sleep(0.05)
    GPIO.output(clk_num, 0)
    sleep(0.05)

def ssdLoop(clk_num): #this constantly scans for input from the keypad 
    if clear == False:
        ssd_disp(clk_num, readKeypad(X1, [1,2,3,'A']))
        ssd_disp(clk_num, readKeypad(X2, [4,5,6,'B']))
        ssd_disp(clk_num, readKeypad(X3, [7,8,9,'C']))
        ssd_disp(clk_num, readKeypad(X4, ['*',0,'#','D']))
        sleep(.1)
    if clear == True:
        ssd_disp(clk_num, readKeypad(X4, ['*',0,'#','D'])) #only reads bottom row, hence only the # button
        sleep(.1)
        
def getTime(now=None): #This gets time from the DateTime library, used in the automatic setup
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
    curr = getTime(current_time) #gets current time 
    ssd_disp(clk1, curr[0]) #sets it to the value from the curr lis
    ssd_disp(clk2, curr[1])
    ssd_disp(clk3, curr[2])
    ssd_disp(clk4, curr[3])
    if curr[4] == True:
        GPIO.output(dot, 1)
    
def manualset():
    global counter, clock, toggle, clear , manual_time, key1, h2, concatenated
    global key2, key3, key4, last1,last2, delays, timer, time_num
    counter = 0
    while counter < 4 and counter >= 0:
        clear = not clear
        switch(clock[counter], dff_pins) #this and the clear make the ssd's flash in the while loop
        if counter == 0: #using a counter which is increased in the ssd_disp function to move on to each ssd setup
            ssdLoop(clk1)
            sleep(.1)
            last1 = [GPIO.input(i) for i in dff_pins]
            keyfinderHH(last1) #gets the key from bin_vals dictionary, repeated for ssd's       
        if counter == 1:
            ssdLoop(clk2)
            sleep(.1)
            last2 = [GPIO.input(i) for i in dff_pins]
            keyfinderH2(last2)
            if concatenated == False:
                manual_get_time() #concatenates the two keys and checks to convert it to 12-hour
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
            if timer == False:
                manual_time = True

    while manual_time == True:
        start = time.time()
        last4 = bin_vals[key4] #stores key value after time changes in delay function 
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
        ssdLoop(clk5) #
        counter = 5
        delays += 1
        for x in range(9300000):
            pass
        if delays == 20: #value based on how long it takes to reach a minute in the loop
            delay()
            delays = 0
        elapsed = time.time() - start
        print(elapsed)
    while timer == True:
        time_num += 1
        if time_num == 20:
            timer_set()
        for x in range(9300000):
            pass
        last4 = bin_vals[key4] #stores key value after time changes in delay function 
        last3 = bin_vals[key3]
        last2 = bin_vals[key2]
        last1 = bin_vals[key1]
        last_dff = [last1,last2,last3,last4]
        for x in range(4):
                output(dff_pins, last_dff[x])
                ssdLoop(clock[x])
        
        ssdLoop(clk5)
        
def manual_get_time():
    global key1, key2, last1,last2, concatenated, dot
    conc = str(key1) + str(key2) #grabs two keys from manual function and compares to 12, then changes and stores accordingly
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
    

def delay(): #function used to add a minute to the clock
    global key1,key2,key3,key4
    global  last1,last2,last3,last4
    key4 +=1
    if key4 > 9: #This nested if statement executes fully at the end of an hour, say 11:59
        key4 = 0
        key3 += 1
        if key3 > 5:
            key3 = 0
            key2 += 1
            if key2 > (9 if key1 == 0 else 2):
                key2 = 0 if key1 == 0 else 1
                key1 ^= 1 #Toggles key1 between 0 and 1
    ssd_disp(clk1, key1)
    ssd_disp(clk2, key2)
    ssd_disp(clk3, key3)
    ssd_disp(clk4, key4)
    
def keyfinderHH(values):
    global key1, counter, invalid, value1 #finds the key to from the value in the bin_vals dictionary
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
    if key1 > 1: #checks if the first of HH is a 2 so that the next value cannot be more than 4 
        if key2 > 4:
            GPIO.output(invalid, 1)
            counter = 1
            
def keyfinderMM(values):
    global key3, two, counter, value3
    for key, value in bin_vals.items(): 
        if value == values:
            key3 = key
            value3 = value
    if key3 > 5: #same as above but with 5
        GPIO.output(invalid, 1)
        counter = 2

def keyfinderM2(values):
    global key4
    for key, value in bin_vals.items():
        if value == values:
            key4 = key
            
def timer_set():   
    global key1,key2,key3,key4
    key4 -= 1 #works like the delay function just with different values for a timer
    if key4 < 0:
        key4 = 9
        key3 -= 1
        if key3 < 0:
            key3 = 5
            key2 -= 1
            if key2 < 0:
                if key1 == 0:
                    key2 = 0
                else:
                    key2 = 9
                    key1 -= 1
                if key1 < 0:
                    key1 = 0
                
    ssd_disp(clk1, key1)
    ssd_disp(clk2, key2)
    ssd_disp(clk3, key3)
    ssd_disp(clk4, key4)
    
current_time = datetime.now()
curr = getTime(current_time)
output(dff_pins, [1,1,1,1,1,1,0,0])
GPIO.output(dot,0)
counter = 100

try:
    while True:

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