from csv import writer

class SeqHandler:
    def __init__(self,path):
        self.name="none"
        self.sequence=[s]

    def read(self):
        print("Running")
        # TODO read and format the CSV sequence file into array of [psi,theta,phi,x,y,z,time] vectors
        import csv
        with open('Maze Solution.csv') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            vectors = []
            for row in csv_reader:
                vectors.append(row)
            print(data[1:])
        return vectors
        #pls delete or modify if it's not what how you want it.
        #also created a separate .csv file without the initial header names to make it easier to write this code

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