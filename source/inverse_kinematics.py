from .input_output import Arduino,SeqHandler
from .Config import mechParams, options
import numpy as np
import time
import tkinter
from pyquaternion import Quaternion
from tkinter.filedialog import askopenfilename
root = tkinter.Tk() #File open dialog
root.withdraw()

class invKinematics:
    def __init__(self):
        self.lengthSequence=[]
        self.baseCoords=[(x1,y1,0), (x2,y2,0)] # need to input base coordinates for all attachment points
        # TODO needs to be parametric using Config.mechParams['radius']
    
    def run(self):
        self.positions=self.SeqHandler.read() #array of position vectors
        for idx,vector in enumerate(self.positions):
            # I assume a positionVector of the form [psi,theta,phi,x,y,z]
            lengths=self.computeLength(vector)
            angles=self.computeAngles(lengths)
            self.lengthSequence.append(lengths)
            for i in self.lengthSequence:
                Arduino.write(i)  # TODO need to format the way this works
                time.sleep(time) # Sleep for the required time
                if not Arduino.read(): #check that the move had been completed
                    break



    def createTransformMatrix(self,rotation):
        psi=np.radians(rotation[0])
        cPsi,sPsi=np.cos(psi),np.sin(psi)

        theta = np.radians(rotation[1])
        cT, sT = np.cos(theta), np.sin(theta)

        phi = np.radians(rotation[2])
        cPhi, sPhi = np.cos(phi), np.sin(phi)

        s=mechParams['scale']
        matrix=np.array([[-s*cPhi*cT,   s*(cPhi*sPsi-cPsi*sT*sPhi),    -s(sPsi*sPhi+cPsi*cPhi*sT)],
                        [-s*cT*sPsi,   -s*(sPsi*sT*sPhi+cPsi*cPhi),    s*(cPsi*sPhi-cPhi*sPsi*sT)],
                        [-s*sT,         s*cT*sPhi,                     s*cT*cPhi,                ],
                         ])
        return matrix

    def quaternionTransform(self,baseVector,rotation,translation):
        baseVector*=mechParams["scale"] #rescale to upper platform
        midZHeight=mechParams['midZHeight']
        q1 = Quaternion(axis=[1, 0, 0], angle=np.radians(rotation[0])) #x rotation, Eulerian Psi, Roll
        q2 = Quaternion(axis=[0, 1, 0], angle=np.radians(rotation[1]))  # y rotation, Eulerian Theta, Pitch
        q3 = Quaternion(axis=[0, 0, 1], angle=np.pi + np.radians(rotation[2]))  # Z rotation, Eulerian phi, Yaw
        # Note that the platform is initially rotated 180 degrees from the base. XYZ axes as per the paper
        qR=q1*q2*q3
        rV=qR.rotate(baseVector) #qaternion rotation
        platformVector=np.add(rV,translation) #add the translation
        platformVector=np.add(midZHeight,platformVector) #add the Z=0 position.
        return platformVector

    def computeLength(self, position):
        lengths=[]
        rotation=position[0:2]
        translation=position[3:5]
        for i,basePoint in enumerate(self.baseCoords):
            if options['transformMode']=="quaternion":
                platformVector = self.quaternionTransform(basePoint,rotation,translation)  # transform to the platform
            else:
                R=self.createTransformMatrix(rotation)
                platformVector=np.dot(basePoint,R) # R o T a T E the vector
                platformVector = np.add(platformVector, translation)  # add the translation
            legLength=np.linalg.norm(platformVector-basePoint) # get length by subtracting base vector
            legLength-=mechParams['defaultLength'] #subtract the length of the syringe itself to obtain a delta
            lengths.append(legLength)
        return lengths

    def computeAngle(self, length):
        #TODO compute the PWM AUDREY
        angle=""
        return angle


def main(): #runs when we start the script
    while True:
        command=input("R to run a solution, M for manual Mode")
        if command == "R":
            try:
                sequence_file = askopenfilename(title="Select sequence file",
                                                filetypes=(("Memes", "*.csv"), ("all files", "*.*")))
            except:
                sequence_file = 0
            kin = invKinematics
            kin.SeqHandler = SeqHandler(sequence_file)
            kin.run()
        elif command == "M":
            while True:
                i=input("Command:")
                if i="servo1":
                    Arduino.write(300)
            #TODO make manual command mode here that tilts in x and y
if __name__ == '__main__':      main()