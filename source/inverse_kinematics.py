from input_output import Arduino,SeqHandler
from Config import mechParams, options
import numpy as np
import time
import tkinter
from pyquaternion import Quaternion
from tkinter.filedialog import askopenfilename
root = tkinter.Tk() #File open dialog
root.withdraw()

class invKinematics:
    def __init__(self,sequencePath):
        self.lengthSequence=[]
        self.csv=SeqHandler(sequencePath)
        self.baseCoords=np.array([[1,1,0], [2,2,0], [3,3,0],[4,4,0],[5,5,0],[6,6,0]]) # need to input base coordinates for all attachment points
        # TODO needs to be parametric using Config.mechParams['radius']
    
    def run(self):
        self.positions=self.csv.read() #array of position vectors
        for idx,vector in enumerate(self.positions):
            # I assume a positionVector of the form [psi,theta,phi,x,y,z,time]
            lengths=self.computeLengths(vector)
            angles=self.computeAngles(lengths) #lengths is a tuple of 6 lengths of the form (L0,L1,L2,L3,L4,L5) in mm defined as positive from the fully retracted position of the syringe.
            for i in self.angles:
                Arduino.write(i) #write each angle to the Arduino
                wait=vector[6]
                time.sleep(wait) # Sleep for the required time to wait for the ball to roll
                if not Arduino.read(): #check that the move had been completed
                    print("No response from Arduino")
                    break



    def createTransformMatrix(self,rotation):
        psi,theta,phi=rotation
        cPsi,sPsi=np.cos(psi),np.sin(psi)
        cT, sT = np.cos(theta), np.sin(theta)
        cPhi, sPhi = np.cos(phi), np.sin(phi)
        s=mechParams['scale']
        matrix=np.array([[-s*cPhi*cT,   s*(cPhi*sPsi-cPsi*sT*sPhi),    -s*(sPsi*sPhi+cPsi*cPhi*sT)],
                        [-s*cT*sPsi,   -s*(sPsi*sT*sPhi+cPsi*cPhi),    s*(cPsi*sPhi-cPhi*sPsi*sT)],
                        [-s*sT,         s*cT*sPhi,                     s*cT*cPhi,                ],
                         ])
        return matrix

    def quaternionTransform(self,baseVector,rotation,translation):
        baseVector=np.multiply(baseVector,mechParams["scale"]) #rescale to upper platform
        midZHeight=mechParams['midZHeight']
        q1 = Quaternion(axis=[1, 0, 0], angle=rotation[0]) #x rotation, Eulerian Psi, Roll
        q2 = Quaternion(axis=[0, 1, 0], angle=rotation[1])  # y rotation, Eulerian Theta, Pitch
        q3 = Quaternion(axis=[0, 0, 1], angle=rotation[2])  # Z rotation, Eulerian phi, Yaw
        # Note that the platform is initially rotated 180 degrees from the base. XYZ axes as per the paper
        qR=q1*q2*q3
        rV=qR.rotate(baseVector) #qaternion rotation
        platformVector=np.add(rV,translation) #add the translation
        platformVector=np.add(midZHeight,platformVector) #add the Z=0 position.
        return platformVector

    def computeLengths(self, position):
        lengths=[]
        rotation=position[0:3]
        rotation=[np.radians(i)for i in rotation] #radians
        rotation[2] += np.pi #add the 180 degree default platform rotation
        translation=position[3:6]
        for i, basePoint in enumerate(self.baseCoords):
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

    def computeAngles(self, length):
        #TODO compute the PWM AUDREY
        #input is a tuple of 6 lengths of the form (L0,L1,L2,L3,L4,L5) in mm defined as positive from the fully retracted position of the syringe.
        angles=""
        return angles #should be a tuple of 6 servo angles between 150 and 280 (a0,a1...,a5)


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
