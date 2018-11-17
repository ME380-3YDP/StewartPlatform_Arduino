import serial
import string

class SeqHandler:
    def __init__(self,path):
        self.path=path
        self.name="none"
        self.sequence=[]

    def read(self):
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
        self.serial=serial.Serial('/dev/ttyACM1', 19200)
    def read(self):
        data=int(self.serial.readline())
        return data

    def write(self,data):
        dataStr=str(data)
        dataStr+=" \n"
        self.serial.write(dataStr.encode())
        response=float(self.serial.readline())
        print("Arduino angle:",response)