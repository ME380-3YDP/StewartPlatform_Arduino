from input_output import Arduino,SeqHandler
from Config import mechParams, options
import numpy as np
import math
import time
import tkinter
from tkinter.filedialog import askopenfilename
root = tkinter.Tk() #File open dialog
root.withdraw()

class invKinematics:
    def __init__(self,sequencePath):
        self.lengthSequence=[]
        self.csv=SeqHandler(sequencePath)
        c15,s15,sqrt2=(np.cos(np.pi/12.0),np.sin(np.pi/12.0),np.sqrt(2)/2.0)
        coordinates= np.array([[-c15, -s15, 0], [-sqrt2, -sqrt2, 0], [sqrt2, -sqrt2, 0], [c15, -s15, 0],[s15, c15, 0],[-s15, c15, 0]])
        self.baseCoords=np.multiply(mechParams['radius'],coordinates)
        baseRadius=mechParams['scale']*mechParams['radius']
        self.platformCoords=np.multiply(baseRadius,coordinates)
    
    def run(self):
        controller=Arduino()
        self.positions=self.csv.read() #array of position vectors
        for idx,vector in enumerate(self.positions):
            # I assume a positionVector of the form [psi,theta,phi,x,y,z,time]
            lengths=self.computeLengths(vector)
            print("Syringe Lengths:",lengths)
            self.angles=self.computeAngles(lengths) #lengths is a list of 6 lengths of the form (L0,L1,L2,L3,L4,L5) in mm defined as positive from the fully retracted position of the syringe.
            for i in self.angles:
                controller.write(i) #write each angle to the Arduino
            print("Moving to", vector)
            wait = vector[6]
            time.sleep(wait)



    def createTransformMatrix(self,rotation):
        psi,theta,phi=rotation
        cPsi,sPsi=np.cos(psi),np.sin(psi)
        cT, sT = np.cos(theta), np.sin(theta)
        cPhi, sPhi = np.cos(phi), np.sin(phi)
        matrix=np.array([[cPhi*cT,   -cPhi*sPsi+cPsi*sT*sPhi,    sPsi*sPhi+cPsi*cPhi*sT],
                        [cT*sPsi,    sPsi*sT*sPhi+cPsi*cPhi,    -cPsi*sPhi+cPhi*sPsi*sT],
                        [-sT,         cT*sPhi,                     cT*cPhi,            ],
                         ])
        return matrix

    def computeLengths(self, position):
        lengths=[]
        rotation=position[0:3]
        #rotation[2] += np.pi  # add the 180 degree default platform rotation
        rotation=[np.radians(i)for i in rotation] #radians
        translation=position[3:6]
        R = self.createTransformMatrix(rotation)
        for i, platformPoint in enumerate(self.platformCoords):
            platformVector=np.dot(R,platformPoint) # R o T a T E the vector
            platformVector = np.add(platformVector, translation)  # add the translation
            hack=[1,0,3,2,5,4]
            platformVector = np.subtract(platformVector, self.baseCoords[hack[i]])
            legLength=np.linalg.norm(platformVector) # get length by subtracting base vector
            legLength-=mechParams['defaultLength'] #subtract the length of the syringe itself to obtain a delta
            lengths.append(legLength)
        return lengths

    def computeAngles(self, lengths):
        range=mechParams['rangeOfMotion']
        lengths=[range-i for i in lengths] # convert the top syringe length to motion at the bottom by subtracting ROM
        angles = []
        a = mechParams['crankLength']
        b = mechParams['conRodLength']
        c_length =[a+b-i for i in lengths]  # starting length when syringe plunger fully enclosed (retracted pos'n)
        for i in c_length:
            inverseanglemath = -(b ** 2 - a ** 2 - (i) ** 2) / (2 * a * (i))
            radians = math.acos(inverseanglemath)
            degrees = math.degrees(radians)
            angles.append(int (degrees*4.0)) #note that this is for 1/4 degree resolution
        return angles #should be a list of 6 servo angles between 0 and 320 (a0,a1...,a5)


def main(): #runs when we start the script
    while True:
        command=input("R to run a solution, M for manual Mode")
        if command == "R":
            try:
                sequence_file = askopenfilename(title="Select sequence file",
                                                filetypes=(("Memes", "*.csv"), ("all files", "*.*")))
            except:
                sequence_file = 0
            kin = invKinematics(sequence_file)
            kin.run()
        elif command == "M":
            while True:
                i=input("Command:")
            #TODO make manual command mode here that tilts in x and y


if __name__ == '__main__':
    main()
