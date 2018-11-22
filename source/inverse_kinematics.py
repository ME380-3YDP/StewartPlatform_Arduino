from input_output import Arduino, SeqHandler
from Config import mechParams, options
import numpy as np
import math
import time
import tkinter
from tkinter.filedialog import askopenfilename

root = tkinter.Tk()  # File open dialog
root.withdraw()


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
        self.controller = Arduino()
        self.positions = self.csv.read()  # array of position vectors
        for idx, vector in enumerate(self.positions):
            # I assume a positionVector of the form [psi,theta,phi,x,y,z,time]
            lengths = self.computeLengths(vector)
            print("Syringe Lengths:", lengths)
            self.angles = self.computeAngles(
                lengths)  # lengths is a list of 6 lengths of the form (L0,L1,L2,L3,L4,L5) in mm defined as positive from the fully retracted position of the syringe.
            for i in self.angles:
                self.controller.write(i)  # write each angle to the Arduino
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


        self.runMANUALMODE(vector)
        c15, s15, sqrt2 = (np.cos(np.pi / 12.0), np.sin(np.pi / 12.0), np.sqrt(2) / 2.0)
        coordinates = np.array(
            [[-c15, -s15, 0], [-sqrt2, -sqrt2, 0], [sqrt2, -sqrt2, 0], [c15, -s15, 0], [s15, c15, 0], [-s15, c15, 0]])
        self.baseCoords = np.multiply(mechParams['radius'], coordinates)
        baseRadius = mechParams['scale'] * mechParams['radius']
        self.platformCoords = np.multiply(baseRadius, coordinates)


    def runMANUALMODE(self,vector):


        controller = Arduino()




            # I assume a positionVector of the form [psi,theta,phi,x,y,z,time]
        lengths = self.computeLengthsMANUALMODE(vector)
        print("Syringe Lengths:", lengths)
        self.angles = self.computeAnglesMANUALMODE(
            lengths)  # lengths is a list of 6 lengths of the form (L0,L1,L2,L3,L4,L5) in mm defined as positive from the fully retracted position of the syringe.
        for i in self.angles:
            controller.write(i)  # write each angle to the Arduino
        print("Moving to", vector)
        wait = vector[6]
        time.sleep(wait)

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

    def computeAnglesMANUALMODE(self, lengths):
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







def main():  # runs when we start the script
    while True:
        command = input("R to run a solution, M for manual Mode")
        if command == "R":
            try:
                sequence_file = askopenfilename(title="Select sequence file",
                                                filetypes=(("Memes", "*.csv"), ("all files", "*.*")))
            except:
                sequence_file = 0
            kin = invKinematics(sequence_file)
            kin.run()
        elif command=="X":
            ard=Arduino()
            solution=np.array([[80.0,80.0,80.0,80.0,80.0,80.0],
                               [25.0,80.0,25.0,80.0,80.0,80.0],
                               [30.0,80.0,25.0,25.0,80.0,80.0],
                               [90.0,60.0,90.0,80.0,25.0,15.0],
                               [30.0,80.0,25.0,25.0,80.0,80.0]])
            for indx,i in enumerate(solution):
                time.sleep(5)
                for angle in i:
                    print(angle)
                    ard.write(angle)  # write each angle to the Arduino
                if indx!=2:
                    time.sleep(3);

        elif command == "M":
            psi=0
            theta=0
            phi=0
            x=0
            y=0
            z=0.23
            t=1
            Yaxisincrement=0
            Xaxisincrement=0
            while True:
                commandtwo = input("Command:")
                if commandtwo == "W":  # ONE degree clockwise (CW) about the Y-AXIS (from perspective of +ve y-axis facing to right and +ve x-axis facing toward you)

                    Yaxisincrement = Yaxisincrement + 1
                    theta = Yaxisincrement


                elif commandtwo == "S":

                    Yaxisincrement = Yaxisincrement - 1
                    theta = Yaxisincrement


                elif commandtwo == "A":
                    Xaxisincrement = Xaxisincrement - 1
                    phi = Xaxisincrement


                elif commandtwo == "D":
                    Xaxisincrement = Xaxisincrement + 1
                    phi = Xaxisincrement

                vector = [psi, theta, phi, x, y, z, t]

                invKinematicsMANUALMODE(vector)
                lengths=kin.computeLengths(vector)
                angles=kin.computeAngles(lengths)
                kin.controller.write(angles)

            # TODO make manual command mode here that tilts in x and y


if __name__ == '__main__':
    main()