#7
from time import sleep
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
LED = 5
speaker = 6
key = 13
timer = 0
#unit_length = float(input('Enter the desired unit length in seconds: '))

GPIO.setup([LED, speaker], GPIO.OUT)
GPIO.setup(key, GPIO.IN)
pwm = GPIO.PWM(speaker, 1000)
# Translations from English to Morse
mc = {'a': '.- ','b': '-... ', 'c': '-.-. ','d': '-.. ','e': '. ',
    'f': '..-. ','g': '--. ','h': '.... ','i': '.. ','j': '.--- ','k': '-.- ',
    'l': '.-.. ','m': '-- ','n': '-. ','o': '--- ', 'p': '.--. ', 'q': '--.- ',
    'r': '.-. ','s': '... ','t': '- ', 'u': '..- ', 'v': '...- ', 'w': '.-- ',
    'x': '-..- ', 'y': '-.-- ', 'z': '--.. ',
    '0': '----- ','1': '.---- ','2': '..--- ','3': '...-- ','4': '....- ',
    '5': '..... ','6': '-.... ','7': '--... ','8': '---.. ','9': '----. ', 'attention':'-.-.-', 'over': '-.-', 'out':'-.-.'    }

mc_decode = {v : k for k,v in mc.items()}
# Translating each character
def translate(char):
    if char not in mc:
        return ' '
    return mc[char]

# Translating words at a time with cases for key words 
def mcword(word):
    if word == 'attention':
        return '-.-.-'
    if word == 'over':
        return '-.-'
    if word == 'out':
        return '.-.-.'
    return ''.join([translate(i) for i in word])


# Write MC output to file
def writeMC(filename, inputfile):
    with open(inputfile) as file:
        lines = [line.rstrip() for line in file.readlines()]
    f = open(filename, 'w')
    f.write(mcword('attention') + '| ' + 'attention' + '\n') 
    for line in lines:
        line = line.split(' ')
        for i in range(len(line)):
            if i == 0:
                f.write(mcword(line[i]) + '| ' + line[i] + '\n')
            else:
                f.write('       ' + mcword(line[i]) + '| ' + line[i] + '\n')
        f.write(mcword('over') + '| ' + 'over' + '\n')
    f.write(mcword('out') + '| ' + 'out' + '\n')
    f.close()
    
# Output to LED 
def beep(delay):
    GPIO.output([LED, speaker], 1)
    sleep(delay)
    GPIO.output([LED, speaker], 0)
    sleep(0.5)

# Different flashing time for dots and dashes
def mc_inp(char):
    if char == '-':
        beep(.5)
    elif char == '.':
        beep(0.25)
    else:
        sleep(0.25)
        
# Read output file and transmit MC through LED        
def mcOut(filename):
    with open(filename) as file:
        lines = [line.rstrip().lstrip().split('|')[0] for line in file.readlines()]
    for line in lines:
        for ch in line:
            mc_inp(ch)


           
def keyTime(channel):
    global timer
    start = timer
    while GPIO.input(channel):
        GPIO.output(LED, 1)
        pwm.start(70)
    GPIO.output(LED, 0)
    pwm.stop()
    end = timer
    return timer

def getSymbol(pressTime, avgdot, avgdash):
    if pressTime <= avgdot and pressTime > 0.0002: return '.'
    elif pressTime >= avgdash or pressTime >= 3*avgdot: return '-'
    



def pauseTime():
    while GPIO.input(key):
        pass
    
    start = time.time()
    while not GPIO.input(key):
        pass

    return time.time() - start
GPIO.add_event_detect(key, GPIO.RISING, callback=keyTime, bouncetime=100)
if __name__ == '__main__':
    avgdot = []

    while len(avgdot) < 5:
        press = keyTime(key)
        if press > 0.001:
            print("Press time: ", press)
            avgdot.append(press)
            sleep(0.01)
#             fn = input('Enter a file to decode: ')
#             writeMC('output.txt', fn)
#             mcOut('output.txt')
    
    dot_length = 0.5 * (avgdot[1] + avgdot[3])
    dash_length = (1/3) * (avgdot[0] + avgdot[2] + avgdot[4])
    print('Dot length: ', dot_length)
    print('Dash length: ', dash_length)
    sleep(1)
    
    
    
    word = ''
    decoded = ''
    with open('mcoutput.txt', 'w') as file:
        try:
            while True:
                press = keyTime(key)
                pause = pauseTime()
#                  print(getSymbol(press, dot_length, dash_length))
#                  if pause >= dash_length: print(' ')
                if press <= dot_length and press > 0.001:
                    file.write('.')
                    print('.')
                    word += '.'
                    
                if press >= dash_length:
                    file.write('-')
                    print('-')
                    word += '-'
                    
                if pause >= 3*dash_length:
                    file.write(word)
                    file.write(' | ')
                    word = word.split()
                    word = [word + ' ' for word in word]
                    print(word)
                    decode = [mc_decode.get(word, '?') for word in word]
                    for n in decode:
                        file.write(n)
                    file.write(' \n')
                    word = ''
                    print('line break')
            
                if pause >= dash_length and pause < 3 * dash_length:
                    file.write(' ')
                    print('space')
                     
                sleep(0.01)
        except KeyboardInterrupt:
            file.close()
            GPIO.cleanup()
