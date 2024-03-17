import simpleaudio as sa
import numpy as np
Frequency = 500 #generated tone will be 500Hz
Fs = 44100 #sampling frequency
seconds = 10 #duration tone will be played for
t=np.linspace(0,seconds,seconds * Fs, False) #generate an array to build a sine wave
note = np.sin(Frequency*t*2*np.pi) #creates the sine wave
audio = note*(2**15-1)/np.max(np.abs(note))  #ensures audio is within output range
audio = audio.astype(np.int16) #converts audio into 16-bit format
playObj=sa.play_buffer(audio,1,2,Fs) #starts audio playback