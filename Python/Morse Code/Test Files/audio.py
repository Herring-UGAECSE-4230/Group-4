import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
speaker = 6
LED = 5
GPIO.setup(speaker, GPIO.OUT)
GPIO.setup(LED, GPIO.OUT)

import simpleaudio as sa
import numpy as np

def play(data, samplerate):
    for i in range(len(data)):
        GPIO.output(speaker, data[i])
        time.sleep(1/samplerate)




try: 
    Frequency = 500 #generated tone will be 500Hz
    Fs = 44100 #sampling frequency
    seconds = 10 #duration tone will be played for
    t=np.linspace(0,seconds,seconds * Fs, False) #generate an array to build a sine wave
    note = np.sin(Frequency*t*2*np.pi) #creates the sine wave
    audio = note*(2**15-1)/np.max(np.abs(note))  #ensures audio is within output range
    audio = audio.astype(np.int16) #converts audio into 16-bit format
    play(audio, Fs)
except:
    GPIO.cleanup()
    