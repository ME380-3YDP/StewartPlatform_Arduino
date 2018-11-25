import serial
import numpy as np
import time
class Arduino:
    def __init__(self):
        self.serial=serial.Serial('/dev/ttyACM0', 19200)
    def read(self):
        data=int(self.serial.readline())
        return data

    def write(self,data):
        dataStr=str(data)
        dataStr+=" \n"
        self.serial.write(dataStr.encode())

controller = Arduino()
time.sleep(3)
sleepy = [5, 4, 4, 4, 4,4]
solution = np.array([
    [80,80,80,80,80,80],
    [25, 25, 80, 90, 60, 40],
    [30, 80, 40, 80, 80, 90],
    [30, 80, 30, 40, 80, 90],
    [30, 30, 80, 60, 30, 40],
    [60, 60, 80, 60, 30, 10]])
for j, step in enumerate(solution):
    angles = step
    for i in angles:
        controller.write(i)  # write each angle to the Arduin
    time.sleep(sleepy[j])