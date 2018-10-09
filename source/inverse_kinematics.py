from input_output import SeqHandler
import numpy as np
import tkinter
import Config
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
            #TODO read through each vector
            # I assume a positionVector of the form [psi,theta,phi,x,y,z]

            lengths=self.computeLenghts(vector)
            self.lengthSequence.append()
        self.SeqHandler.write(self.lengthSequence) #output to file

    def createTransformMatrix(self,rotation,translation):
        psi=np.radians(rotation[0])
        cPsi,sPsi=np.cos(psi),np.sin(psi)

        theta = np.radians(rotation[1])
        cT, sT = np.cos(theta), np.sin(theta)

        phi = np.radians(rotation[2])
        cPhi, sPhi = np.cos(phi), np.sin(phi)

        x,y,z=translation # unpack
        s=Config.mechParams['scale']
        matrix=np.array([[-s*cPhi*cT,   s*(cPhi*sPsi-cPsi*sT*sPhi),    -s(sPsi*sPhi+cPsi*cPhi*sT),  x],
                                [-s*cT*sPsi,   -s*(sPsi*sT*sPhi+cPsi*cPhi),    s*(cPsi*sPhi-cPhi*sPsi*sT),  y],
                                [-s*sT,         s*cT*sPhi,                     s*cT*cPhi,                   z],
                                [0,             0,                              0,                          1]])
        #this looks terrible
        return matrix

    def quaternionTransform(self,baseVector,rotation,translation):
        baseVector*=Config.mechParams["scale"] #rescale to upper platform
        midZHeight=Config.mechParams['midZHeight']
        q1 = Quaternion(axis=[1, 0, 0], angle=np.radians(rotation[0])) #x rotation, Eulerian Psi, Roll
        q2 = Quaternion(axis=[0, 1, 0], angle=np.radians(rotation[1]))  # y rotation, Eulerian Theta, Pitch
        q3 = Quaternion(axis=[0, 0, 1], angle=np.pi + np.radians(rotation[2]))  # Z rotation, Eulerian phi, Yaw
        # Note that the platform is initially rotated 180 degrees from the base. XYZ axes as per the paper
        qR=q1*q2*q3
        rV=qR.rotate(baseVector) #qaternion rotation
        platformVector=np.add(rV,translation) #add the translation
        platformVector=np.add(midZHeight,platformVector) #add the Z=0 position.
        return platformVector

    def computeLenghts(self, position):
        lengths=[]
        rotation=position[0:2]
        translation=position[3:5]
        for i,basePoint in enumerate(self.baseCoords):
            if Config.options['transformMode']=="quaternion":
                platformVector = self.quaternionTransform(basePoint,rotation,translation)  # transform to the platform
            else
                R=self.createTransformMatrix(rotation,translation)
                platformvector=np.dot(basePoint,R) # not sure if this is right
            legLength=np.linalg.norm(platformvector-np.take(self.baseCoords,i-3,mode="wrap")) # directly implementing the paper, not sure why this is done
            legLength-=Config.mechParams['defaultLength'] #subtract the length of the syringe itself to obtain a delta
            lengths.append(legLength)
        return lengths



def main(): #runs when we start the script
    try:
        sequence_file =askopenfilename(title = "Select sequence file",filetypes = (("Memes","*.csv"),("all files","*.*")))
    except:
        sequence_file = 0

    print(__doc__)
    invKinematics.SeqHandler=SeqHandler(sequence_file)

if __name__ == '__main__':
    main()