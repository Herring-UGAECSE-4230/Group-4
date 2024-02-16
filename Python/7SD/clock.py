import RPi.GPIO as GPIO 
GPIO.setmode(GPIO.BCM)
X1 = 17
X2 = 27
X3 = 22
X4 = 5
Y1 = 6
Y2 = 13
Y3 = 16
Y4 = 12
GPIO.setup([X1,X2,X3,X4], GPIO.OUT)
GPIO.setup([Y1,Y2,Y3,Y4], GPIO.IN)

def readKeypad(rowNum,char):
	curVal = ""
	GPIO.output(rowNum,GPIO.HIGH)
	if GPIO.input(Y1)==1: curVal=char[0]
	if GPIO.input(Y2)==1: curVal=char[1]
	if GPIO.input(Y3)==1: curVal=char[2]
	if GPIO.input(Y4)==1: curVal=char[3]
	GPIO.output(rowNum,GPIO.LOW)
	return curVal

while True:
	try:
		print(readKeypad(X1, [1,2,3,'A']))

		print(readKeypad(X2, [4,5,6,'B']))

		print(readKeypad(X3, [7,8,9,'C']))

		print(readKeypad(X4, ["*",0,"#",'D']))
	except KeyboardInterrupt: 
		GPIO.cleanup()
