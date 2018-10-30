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
        c15,s15,sqrt2=(np.cos(np.pi/12.0),np.sin(np.pi/12.0),np.sqrt(2)/2.0)
        coordinates= np.array([[-c15, -s15, 0], [-sqrt2, -sqrt2, 0], [sqrt2, -sqrt2, 0], [c15, -s15, 0],[s15, c15, 0],[-s15, c15, 0]])
        self.baseCoords=np.multiply(mechParams['radius'],coordinates)
        baseRadius=mechParams['scale']*mechParams['radius']
        self.platformCoords=np.multiply(baseRadius,coordinates)
    
    def run(self):
        self.positions=self.csv.read() #array of position vectors
        for idx,vector in enumerate(self.positions):
            # I assume a positionVector of the form [psi,theta,phi,x,y,z,time]
            lengths=self.computeLengths(vector)
            print(lengths)
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
        matrix=np.array([[cPhi*cT,   -cPhi*sPsi+cPsi*sT*sPhi,    sPsi*sPhi+cPsi*cPhi*sT],
                        [cT*sPsi,    sPsi*sT*sPhi+cPsi*cPhi,    -cPsi*sPhi+cPhi*sPsi*sT],
                        [-sT,         cT*sPhi,                     cT*cPhi,            ],
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
        #platformVector=np.add(midZHeight,platformVector) #add the Z=0 position.
        return platformVector

    def computeLengths(self, position):
        lengths=[]
        rotation=position[0:3]
        #rotation[2] += np.pi  # add the 180 degree default platform rotation
        rotation=[np.radians(i)for i in rotation] #radians
        translation=position[3:6]
        R = self.createTransformMatrix(rotation)
        for i, platformPoint in enumerate(self.platformCoords):
            if options['transformMode']=="quaternion":
                platformVector = self.quaternionTransform(platformPoint,rotation,translation)  # transform to the platform
            else:
                platformVector=np.dot(R,platformPoint) # R o T a T E the vector
                platformVector = np.add(platformVector, translation)  # add the translation
                hack=[1,0,3,2,5,4]
            platformVector = np.subtract(platformVector, self.baseCoords[hack[i]])
            legLength=np.linalg.norm(platformVector) # get length by subtracting base vector
            #legLength-=mechParams['defaultLength'] #subtract the length of the syringe itself to obtain a delta
            lengths.append(legLength)
        return lengths

    def computeAngles(self, length):
        #CODE - WAIT UNTIL ALL LENGTHS L0...L5 HAVE BEEN INPUTTED 
        angles=[]
        a = 0.0035 #length of crank, subject to change. This is measured with the hole spacing center to center (last clearance hole to the hole that connects to the conrod)
        b = 0.0090 #length of con rod, subject to change (center to center distance) 
        c = [a+b, a+b, a+b, a+b, a+b, a+b] #starting length when syringe plunger fully enclosed (retracted pos'n)
        print(length)
        c_length =[]
        c_length =np.subtract(c, length) #length to use for cosine law
        print(c_length)
        inverseangle=[]
        for i in c_length:
            inverseanglemath= -(-b**2 - a**2 + (i)**2)/(2*a*b)
            print(inverseanglemath)
            calculation= math.acos(inverseanglemath)
            angles.append(calculation)
            #TODO convert to PWN 
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
