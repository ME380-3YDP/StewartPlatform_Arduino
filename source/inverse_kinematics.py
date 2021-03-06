from input_output import Arduino, SeqHandler
from Config import mechParams, options
import numpy as np
import math
import time
import tkinter
import datetime
import msvcrt

#key presses here
from tkinter.filedialog import askopenfilename

root = tkinter.Tk()  # File open dialog
root.withdraw()

psi = 3
theta = 3
phi = 3
x = 0
y = 0
z = 0.23
t = 1
Yaxisincrement = 3
Xaxisincrement = 3



def key_bind(event):                   #key_bind defines key binding function
    commandtwo = event.keysym.lower()
    print(commandtwo)
    increment = 1;

    # commandtwo = input("Command:") commented out, only needed if using enter instead of key binding

    if commandtwo == "w":  # ONE degree clockwise (CW) about the Y-AXIS (from perspective of +ve y-axis facing to right and +ve x-axis facing toward you)
        global Yaxisincrement
        Yaxisincrement += increment



    elif commandtwo == "s":
        Yaxisincrement = Yaxisincrement - increment



    elif commandtwo == "a":
         global Xaxisincrement
         Xaxisincrement = Xaxisincrement - increment



    elif commandtwo == "d":
        Xaxisincrement = Xaxisincrement + increment


    vector = [psi, Yaxisincrement, Xaxisincrement, x, y, z, t]

    c = invKinematicsMANUALMODE(vector)

    # I assume a positionVector of the form [psi,theta,phi,x,y,z,time]
    lengths = c.computeLengthsMANUALMODE(vector)
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print(commandtwo)
    print(st)
    print("Syringe Lengths:", lengths)
    angles = c.computeAnglesMANUALMODE(
        lengths)  # lengths is a list of 6 lengths of the form (L0,L1,L2,L3,L4,L5) in mm defined as positive from the fully retracted position of the syringe.

    for i in angles:
        controller.write(i)  # write each angle to the Arduino
        #print("Passing to arduino", i)
    print("Moving to", vector)
    wait = vector[6]
    time.sleep(wait)

class invKinematics:
    def __init__(self, sequencePath):
        self.lengthSequence = []
        self.csv = SeqHandler(sequencePath)
        c15, s15, sqrt2 = (np.cos(np.pi / 12.0), np.sin(np.pi / 12.0), np.sqrt(2) / 2.0)
        coordinates = np.array(
            [[-c15, -s15, 0], [-sqrt2, -sqrt2, 0], [sqrt2, -sqrt2, 0], [c15, -s15, 0], [s15, c15, 0], [-s15, c15, 0]])
        self.baseCoords = np.multiply(mechParams['radius'], coordinates)
        baseRadius = mechParams['scale'] * mechParams['radius']
        self.platformCoords = np.multiply(baseRadius, coordinates)

    def run(self):
        controller = Arduino()
        self.positions = self.csv.read()  # array of position vectors
        for idx, vector in enumerate(self.positions):
            # I assume a positionVector of the form [psi,theta,phi,x,y,z,time]
            lengths = self.computeLengths(vector)
            print("Syringe Lengths:", lengths)
            self.angles = self.computeAngles(
                lengths)  # lengths is a list of 6 lengths of the form (L0,L1,L2,L3,L4,L5) in mm defined as positive from the fully retracted position of the syringe.
            for i in self.angles:
                controller.write(i)  # write each angle to the Arduino
            print("Moving to", vector)
            wait = vector[6]
            time.sleep(wait)

    def createTransformMatrix(self, rotation):
        psi, theta, phi = rotation
        cPsi, sPsi = np.cos(psi), np.sin(psi)
        cT, sT = np.cos(theta), np.sin(theta)
        cPhi, sPhi = np.cos(phi), np.sin(phi)
        matrix = np.array([[cPhi * cT, -cPhi * sPsi + cPsi * sT * sPhi, sPsi * sPhi + cPsi * cPhi * sT],
                           [cT * sPsi, sPsi * sT * sPhi + cPsi * cPhi, -cPsi * sPhi + cPhi * sPsi * sT],
                           [-sT, cT * sPhi, cT * cPhi, ],
                           ])
        return matrix

    def computeLengths(self, position):
        lengths = []
        rotation = position[0:3]
        # rotation[2] += np.pi  # add the 180 degree default platform rotation
        rotation = [np.radians(i) for i in rotation]  # radians
        translation = position[3:6]
        R = self.createTransformMatrix(rotation)
        for i, platformPoint in enumerate(self.platformCoords):
            platformVector = np.dot(R, platformPoint)  # R o T a T E the vector
            platformVector = np.add(platformVector, translation)  # add the translation
            hack = [1, 0, 3, 2, 5, 4]
            platformVector = np.subtract(platformVector, self.baseCoords[hack[i]])
            legLength = np.linalg.norm(platformVector)  # get length by subtracting base vector
            legLength -= mechParams['defaultLength']  # subtract the length of the syringe itself to obtain a delta
            lengths.append(legLength)
        return lengths

    def computeAngles(self, lengths):
        range = mechParams['rangeOfMotion']
        if any(t < 0 or t > range for t in lengths):
            print("ERROR, lengths out of ROM", lengths)
            exit()
        lengths = [range - i for i in
                   lengths]  # convert the top syringe length to motion at the bottom by subtracting ROM

        angles = []
        a = mechParams['crankLength']
        b = mechParams['conRodLength']
        c_length = [a + b - i for i in lengths]  # starting length when syringe plunger fully enclosed (retracted pos'n)
        for i in c_length:
            inverseanglemath = -(b ** 2 - a ** 2 - (i) ** 2) / (2 * a * (i))
            radians = math.acos(inverseanglemath)
            degrees = math.degrees(radians)
            angles.append(degrees)
        return angles  # should be a list of 6 servo angles between 0 and 320 (a0,a1...,a5)

class invKinematicsMANUALMODE:

    def __init__(self,vector):


        #self.runMANUALMODE(vector)
        c15, s15, sqrt2 = (np.cos(np.pi / 12.0), np.sin(np.pi / 12.0), np.sqrt(2) / 2.0)
        coordinates = np.array(
            [[-c15, -s15, 0], [-sqrt2, -sqrt2, 0], [sqrt2, -sqrt2, 0], [c15, -s15, 0], [s15, c15, 0], [-s15, c15, 0]])
        self.baseCoords = np.multiply(mechParams['radius'], coordinates)
        baseRadius = mechParams['scale'] * mechParams['radius']
        self.platformCoords = np.multiply(baseRadius, coordinates)



    def createTransformMatrixMANUALMODE(self, rotation):
        psi, theta, phi = rotation
        cPsi, sPsi = np.cos(psi), np.sin(psi)
        cT, sT = np.cos(theta), np.sin(theta)
        cPhi, sPhi = np.cos(phi), np.sin(phi)
        matrix = np.array([[cPhi * cT, -cPhi * sPsi + cPsi * sT * sPhi, sPsi * sPhi + cPsi * cPhi * sT],
                           [cT * sPsi, sPsi * sT * sPhi + cPsi * cPhi, -cPsi * sPhi + cPhi * sPsi * sT],
                           [-sT, cT * sPhi, cT * cPhi, ],
                           ])
        return matrix

    def computeLengthsMANUALMODE(self, position):
        lengths = []
        rotation = position[0:3]
        # rotation[2] += np.pi  # add the 180 degree default platform rotationW
        rotation = [np.radians(i) for i in rotation]  # radians
        translation = position[3:6]
        R = self.createTransformMatrixMANUALMODE(rotation)
        c15, s15, sqrt2 = (np.cos(np.pi / 12.0), np.sin(np.pi / 12.0), np.sqrt(2) / 2.0)
        baseRadius = mechParams['scale'] * mechParams['radius']
        coordinates = np.array(
            [[-c15, -s15, 0], [-sqrt2, -sqrt2, 0], [sqrt2, -sqrt2, 0], [c15, -s15, 0], [s15, c15, 0], [-s15, c15, 0]])
        self.platformCoords = np.multiply(baseRadius, coordinates)
        self.baseCoords = np.multiply(mechParams['radius'], coordinates)
        for i, platformPoint in enumerate(self.platformCoords):
            platformVector = np.dot(R, platformPoint)  # R o T a T E the vector
            platformVector = np.add(platformVector, translation)  # add the translation
            hack = [1, 0, 3, 2, 5, 4]
            platformVector = np.subtract(platformVector, self.baseCoords[hack[i]])
            legLength = np.linalg.norm(platformVector)  # get length by subtracting base vector
            legLength -= mechParams['defaultLength']  # subtract the length of the syringe itself to obtain a delta
            lengths.append(legLength)
        return lengths

    def computeAnglesMANUALMODE(self,lengths):
        range = mechParams['rangeOfMotion']
        if any(t < 0 or t > range for t in lengths):
            print("ERROR, lengths out of ROM", lengths)
            #exit()
        lengths = [range - i for i in
                   lengths]  # convert the top syringe length to motion at the bottom by subtracting ROM

        angles = []
        a = mechParams['crankLength']
        b = mechParams['conRodLength']
        c_length = [a + b - i for i in lengths]  # starting length when syringe plunger fully enclosed (retracted pos'n)
        for i in c_length:
            if i > a + b:
                i = a + b
                inverseanglemath = -(b ** 2 - a ** 2 - (i) ** 2) / (2 * a * (i))
                radians = math.acos(inverseanglemath)
                degrees = math.degrees(radians)
                angles.append(degrees)
                print("crank/con-rod length exceeded")

            elif i == 0:
                angles.append(90)
                print("90 degree crank/con-rod angle reached or exceeded")

            else:
                inverseanglemath = -(b ** 2 - a ** 2 - (i) ** 2) / (2 * a * (i))
                radians = math.acos(inverseanglemath)
                degrees = math.degrees(radians)
                angles.append(degrees)

        return angles








def main():  # runs when we start the script
    command = input("R to run a solution, M for manual Mode")
    if command == "R":
        try:
            sequence_file = askopenfilename(title="Select sequence file",
                                            filetypes=(("Memes", "*.csv"), ("all files", "*.*")))
        except:
            sequence_file = 0
        kin = invKinematics(sequence_file)
        kin.run()
    elif command == "M":
        global controller
        controller = Arduino()

        command = tkinter.Tk()                  #these three lines control keybinding
        command.bind_all("<Key>", key_bind)
        command.mainloop()





            #while True: Audrey's old endless loop now obsolete






if __name__ == '__main__':
    main()