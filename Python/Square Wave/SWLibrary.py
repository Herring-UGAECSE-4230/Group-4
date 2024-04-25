import os
from time import sleep
import subprocess as sp

class SquareWave: #square wave 
    def __init__(self, frequency):
        self.frequency = frequency

    def start(self):
        asm_file_path = '/home/pi/Desktop/Group-4/Python/Square Wave/BIT_BANG'
        os.chdir('/home/pi/Desktop/Group-4/Python/Square Wave/')  #pi4 path 
        sp.Popen('make', shell=False, stdout=sp.PIPE, stderr=sp.DEVNULL).wait()
        self.p1 = sp.Popen([asm_file_path], shell=False, stdout=sp.PIPE, stderr=sp.DEVNULL)

    def stop(self):
        if hasattr(self, 'p1') and self.p1.poll() is None:
            self.p1.terminate()

    def set_frequency(self, frequency):
        self.frequency = frequency
        delay = 10 # Calculate new delay value
        asm_file_path = '/home/pi/Desktop/Group-4/Python/Square Wave/'  #pi4
        with open(asm_file_path, 'r') as file:
            lines = [line.rstrip() for line in file.readlines()]

        for i, line in enumerate(lines):
            print(line)
            if 'DCOUNT,' in line:
                lines[i] = 'DCOUNT,' + str(delay) + '\\n'

        with open(asm_file_path, 'w') as file:
            for line in lines:
                file.write(line + '\n')
                
        sp.Popen('make', shell=False, stdout=sp.PIPE, stderr=sp.DEVNULL).wait()
        #Recompiles file with new frequency

wave = SquareWave(100)
wave.start()
sleep(5)
wave.stop()

