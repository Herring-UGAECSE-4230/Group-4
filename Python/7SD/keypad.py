import RPi.GPIO as GPIO 
GPIO.setmode(GPIO.BCM)
from time import sleep

X1 = 26
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

clk = 18
#ctrl = 26
dff_pins = [a,b,c,d,e,f,g]
GPIO.setup([X1,X2,X3,X4, dot], GPIO.OUT)
GPIO.setup([Y1,Y2,Y3,Y4], GPIO.IN)
GPIO.setup(dff_pins, GPIO.OUT)
GPIO.setup(clk, GPIO.OUT)

def readKeypad(rowNum,char):
	curVal = ""
	GPIO.output(rowNum,GPIO.HIGH)
	if GPIO.input(Y1)==1: curVal=char[0]
	if GPIO.input(Y2)==1: curVal=char[1]
	if GPIO.input(Y3)==1: curVal=char[2]
	if GPIO.input(Y4)==1: curVal=char[3]
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

def output(gpio_lst, states):
	for i in range(len(gpio_lst)):
		GPIO.output(gpio_lst[i], states[i])
		
def switch(gpio_lst):
    last_states = [GPIO.input(i) for i in dff_pins]
    if 1 in last_states: output(gpio_lst, [0,0,0,0,0,0,0])    
    else: output(gpio_lst, last_states)

def ssd_disp(clk_num, value):
    try:
        value = int(value)
        output(dff_pins, bin_vals[value])
    except:
        if value == 'A': output(dff_pins, bin_vals['A'])
        if value == 'B': output(dff_pins, bin_vals['B'])
        if value == 'C': output(dff_pins, bin_vals['C'])
        if value == 'D': output(dff_pins, bin_vals['D'])
        if value == '*':
            if GPIO.input(dot) == 0: GPIO.output(dot, 1)
            else: GPIO.output(dot, 0)
        if value == '#':
            switch(dff_pins)
            
        pass


def latch_value():
	GPIO.output(clk, 1)
	sleep(0.05)
	GPIO.output(clk, 0)

try:
	while True:
		#output2(dff_pins, bin_vals[2])
		#print(readKeypad(X1, [1,2,3,'A']))
        #print(readKeypad(X2, [4,5,6,'B']))
		#print(readKeypad(X3, [7,8,9,'C']))
		#print(readKeypad(X4, ["*",0,"#",'D']))
		#ssd_disp(dff_pins,)
		ssd_disp(clk, readKeypad(X1, [1,2,3,'A']))
		ssd_disp(clk, readKeypad(X2, [4,5,6,'B']))
		ssd_disp(clk, readKeypad(X3, [7,8,9,'C']))
		ssd_disp(clk, readKeypad(X4, ['*',0,'#','D']))
		latch_value()
		sleep(.2)
		
            
		# for i in range(len(dff_pins)):
		# 	GPIO.output(dff_pins[i], bin_vals[1][i])
except KeyboardInterrupt: 
	GPIO.cleanup()