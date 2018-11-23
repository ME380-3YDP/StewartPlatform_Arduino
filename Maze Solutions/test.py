import csv
with open('Maze Solution.csv') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    data = []
    for row in csv_reader:
        data.append(row)
    print('rows are [psi,theta,phi,x,y,z,time] vectors')
    print(data[1:])



