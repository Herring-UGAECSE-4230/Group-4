from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
pin = 16
GPIO.setup(pin, GPIO.OUT)

def beep(delay):
    GPIO.output(pin, 1)
    sleep(delay)
    GPIO.output(pin, 0)
    sleep(0.5)
    
def mc_inp(char):
    if char == '-':
        beep(.5)
    elif char == '.':
        beep(0.25)
    else:
        sleep(0.25)
        
test = '..--'
# 
# for i in test:
#     mc_inp(i)
#

with open('output.txt') as file:
    lines = [line.rstrip().lstrip().split('|')[0] for line in file.readlines()]
    
for line in lines:
    print(line)
    
for line in lines:
    for ch in line:
        mc_inp(ch)