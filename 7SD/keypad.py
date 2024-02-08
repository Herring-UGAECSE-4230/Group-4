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

o1 = 4
o2 = 17
o3 = 27
o4 = 22
o5 = 5
o6 = 6
o7 = 13
o8 = 19

clk = 18
#ctrl = 26
dff_pins = [o8,o7,o6,o5,o4,o3,o2,o1]
GPIO.setup([X1,X2,X3,X4], GPIO.OUT)
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

bin_vals = {0:[1,1,1,1,1,1,0,0], 
			1:[0,0,0,1,0,1,0,0], 
			2:[0,1,0,1,0,0,1,0], 
			3:[1,0,1,1,0,1,1,0], 
			4:[1,1,0,1,1,1,0,0], 
			5:[1,0,1,1,0,1,1,0], 
			6:[1,0,1,1,1,1,1,0], 
			7:[1,1,1,0,0,0,0,0], 
			8:[1,1,1,1,1,1,1,0], 
			9:[1,1,1,1,0,1,1,0]
            }
'''
            'A':[1,1,1,1,1,1,1,1],
            'B':[0,0,0,0,0,0,1,1],
            'C':[0,1,0,1,0,1,0,1],
            'D':[0,1,1,1,0,1,0,1]
            }
'''
def output(gpio_lst, states):
	for i in range(len(gpio_lst)):
		GPIO.output(gpio_lst[i], states[i])

def ssd_disp(clk_num, value):
	try:
		value = int(value)
		output(dff_pins, bin_vals[value])
	except:
		pass


def latch_value():
	GPIO.output(clk, 1)
	sleep(0.01)
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
		latch_value()
		sleep(1)
		# for i in range(len(dff_pins)):
		# 	GPIO.output(dff_pins[i], bin_vals[1][i])
except KeyboardInterrupt: 
	GPIO.cleanup()