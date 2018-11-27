import serial
import numpy as np
import time
class Arduino:
    def __init__(self):
        self.serial=serial.Serial('/dev/ttyACM1', 19200)
    def read(self):
        data=int(self.serial.readline())
        return data

    def write(self,data):
        dataStr=str(data)
        dataStr+=" \n"
        self.serial.write(dataStr.encode())

controller = Arduino()
time.sleep(3)
sleepy = [4, 4, 4, 4,4,4]
solution = np.array([
    [20, 80, 20, 80, 80, 80],
    [80, 80, 30, 30, 80, 80],
    [60, 80, 60, 80, 80, 80],
    [60, 60, 80, 80, 80, 80],
    [60, 35, 90, 90, 40, 20],
    [90, 90, 30, 30, 70, 70],
    [90, 60, 80, 80, 80, 40],
])
for j, step in enumerate(solution):
    angles = step
    for i in angles:
        controller.write(i)  # write each angle to the Arduin
    time.sleep(sleepy[j])