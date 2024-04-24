import os
import subprocess
from time import sleep

class SquareWave: #square wave 
    def __init__(self, frequency):
        self.frequency = frequency

    def update_delay(self, new_delay_value):
        asm_file_path = '/home/pi/Desktop/Group-4/Python/Square Wave/GPIO Off/'  #pi4
        with open(asm_file_path, 'r') as file:
            lines = [line.rstrip() for line in file.readlines()]

        for i, line in enumerate(lines):
            if 'variableName' in line:
                lines[i] = 'variableName:  .asciz ' + str(new_delay_value) + '\\n'

        with open(asm_file_path, 'w') as file:
            for line in lines:
                file.write(line + '\n')

    def start(self):
        os.chdir('/home/pi/Desktop/Group-4/Python/Square Wave/GPIO Off/')  #pi4 path 
        subprocess.Popen('make', shell=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).wait()
        self.p1 = subprocess.Popen('GPIO_ON.s', shell=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    def stop(self):
        if hasattr(self, 'p1') and self.p1.poll() is None:
            self.p1.terminate()

    def set_frequency(self, frequency):
        self.frequency = frequency
        new_delay_value = 0 # Calculate new delay value
        self.update_delay(new_delay_value)
        subprocess.Popen('make', shell=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).wait()
        #Recompiles file with new frequency

wave = SquareWave(100)
wave.start()
sleep(5)
wave.stop()
