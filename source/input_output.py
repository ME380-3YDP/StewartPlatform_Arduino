from csv import writer

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