from csv import writer

class SeqHandler:
    def __init__(self,path):
        self.name="none"
        self.sequence=[]

    def read(self):
        print("Running")
        # TODO read and format the CSV sequence file into array of [psi,theta,phi,x,y,z,time] vectors
        import csv
        with open('Maze Solution.csv', 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            line_count=0
            for row in csv_reader:
                if line_count==0:
                    print (f'Array is formatted as [psi,theta,phi,x,y,z,time] vectors')
                    line_count +=1
                else:
                    data=[]
                    for row in csv_reader:
                        data.append(row)
            print(data[1:])
        # I wrote this, pls delete or modify if it's not what how you want it

     
    def write(self):
        # TODO write a nice array for the arduino to read. Probably txt or CSV
        return 1
