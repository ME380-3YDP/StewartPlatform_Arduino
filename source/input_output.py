from csv import writer

class SeqHandler:
    def __init__(self,path):
        self.name="none"
        self.sequence=[]

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
            
        #pls delete or modify if it's not what how you want it.
        #also created a separate .csv file without the initial header names to make it easier to write this code

     
    def write(self):
        # TODO write a nice array for the arduino to read. Probably txt or CSV
        return 1
