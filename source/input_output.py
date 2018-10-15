from csv import writer
import serial
import struct

class SeqHandler:
    def __init__(self,path):
        self.name="none"
        self.sequence=[]

    def read(self):
        print("Running")
        # TODO read and format the CSV sequence file into array of [psi,theta,phi,x,y,z,time] vectors
        return self.sequence
     
    def write(self):
        # TODO write a nice array for the arduino to read. Probably txt or CSV
        return 1
class Arduino:
    def __init__(self):
        self.serial=serial.Serial('/dev/ttyACM1', 9600)

    def read(self):
        data=self.serial.readline()
        return data

    def write(data):
        if type(data)==int:
            self.serial.write(struct.pack('>B', data)) # this works for all integers, tested it
            response=int(testSer.readline())
        return response