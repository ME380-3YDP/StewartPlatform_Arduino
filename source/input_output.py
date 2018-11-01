import serial
import struct

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
        self.serial=serial.Serial('/dev/ttyACM1', 9600)
    def read(self):
        data=int(self.serial.readline())
        return data
    def write(self,data):
        if type(data)==float and data < 255:
            self.serial.write(struct.pack('>B', data)) # pending test on floating points
            response=int(self.serial.readline())
        else:
            print("Data out of range",data)
        return response