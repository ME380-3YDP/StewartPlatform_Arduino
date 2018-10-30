from csv import writer

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
        data=self.serial.readline()
        return data
    def write(data):
        if type(data)==int:
            self.serial.write(struct.pack('>B', data)) # this works for all integers, tested it
            response=int(testSer.readline())
        return response