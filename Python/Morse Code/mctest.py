from time import sleep
from time import perf_counter
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
LED = 5
speaker = 6
unit_length = float(input('Enter the desired unit length in seconds: '))

GPIO.setup([LED, speaker], GPIO.OUT)

def beep(delay):
    GPIO.output([LED, speaker], 1)
    sleep(delay)
    GPIO.output([LED, speaker], 0)
    sleep(0.5)
    
def mc_inp(char):
    if char == '-':
        beep(2*unit_length)
    elif char == '.':
        beep(unit_length)
    else:
        sleep(0.25)
        


with open('output.txt') as file:
    lines = [line.rstrip().lstrip().split('|')[0] for line in file.readlines()]
    
    
for line in lines:
    print(line)
    for ch in line:
        
#         time1 = perf_counter()
        mc_inp(ch)
#         time2 = perf_counter()
#         print("Time elapsed: ", time2 - time1)