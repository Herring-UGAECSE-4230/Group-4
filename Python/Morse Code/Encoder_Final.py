from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
LED = 5
speaker = 6
unit_length = float(input('Enter the desired unit length in seconds: '))

GPIO.setup([LED,speaker], GPIO.OUT)

pwm = GPIO.PWM(speaker, 1000)
# Translations from English to Morse
mc = {'a': '.- ','b': '-... ', 'c': '-.-. ','d': '-.. ','e': '. ',
    'f': '..-. ','g': '--. ','h': '.... ','i': '.. ','j': '.--- ','k': '-.- ',
    'l': '.-.. ','m': '-- ','n': '-. ','o': '--- ', 'p': '.--. ', 'q': '--.- ',
    'r': '.-. ','s': '... ','t': '- ', 'u': '..- ', 'v': '...- ', 'w': '.-- ',
    'x': '-..- ', 'y': '-.-- ', 'z': '--.. ',
    '0': '----- ','1': '.---- ','2': '..--- ','3': '...-- ','4': '....- ',
    '5': '..... ','6': '-.... ','7': '--... ','8': '---.. ','9': '----. '    }

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
    GPIO.output(LED, 1)
    pwm.start(50)
    sleep(delay)
    GPIO.output(LED, 0)
    pwm.stop()
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
    
try:
    while True:
        fn = input('Enter a file to decode: ')
        writeMC('output.txt', fn)
        mcOut('output.txt')
except KeyboardInterrupt:
    GPIO.cleanup()
    

