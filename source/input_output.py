import serial
import struct
import time

class SeqHandler:
    def __init__(self,path):
        self.path=path
        self.name="none"
        self.sequence=[]

    def read(self):
        print("Reading")
        import csv
        with open(self.path) as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            vectors = []
            for row in csv_reader:
                row = [float(i) for i in row] #convert to floats
                vectors.append(row)
                print(row)
        return vectors

class Arduino:
    def __init__(self):
        self.serial=serial.Serial('/dev/ttyACM0', 9600)
    def read(self):
        data=int(self.serial.readline())
        return data
    def write(self,data):
        if type(data)==int and data < 255:
            time.sleep(1)
            self.serial.write(struct.pack('<B', data))
            #response=int(self.serial.readline())
            #print(response)
        else:
            print("Data out of range",data)