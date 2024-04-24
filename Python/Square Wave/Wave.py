from time import sleep
from SWLibrary import SquareWave as sqWave

print("100 hz")
sqWave.start(100)
sleep(10)
sqWave.stop()

print("1k hz")
sqWave.setFrequency(1000)
sleep(10)
sqWave.stop()

print("program ended")
