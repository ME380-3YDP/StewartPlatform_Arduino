#def computeAangles(self, length):
        #input tuple of 6 lengths of the form (L0,L1,L2,L3,L4,L5) in mm defined as positive from the fully retracted position of the syringe.
import numpy as np
import math

length = [1, 2, 3, 4, 5, 6] #to be removed with def and real shiz once code is complete
angles=[]
a = 0.035 #length of crank, subject to change
b = 0.0075 #length of con rod, subject to change
c = [a+b, a+b, a+b, a+b, a+b, a+b] #starting length when syringe plunger fully enclosed (retracted pos'n)
print(length)
c_length =[]
c_length =np.subtract(c, length) #so we can use trig functions
print(c_length)
inverseanglemath=[]
inverseangle=[]
anglecalculation=[]
for i in c_length:
    inverseanglemath= (-(b**2 - a**2 - (i)**2)/(2*a*(i))

    for j in c_length:
        anglecalculation= np.arccos(inverseanglemath(i))
    #inverseangle.append(inverseanglemath)
    #print(inverseangle)
    angles.append(anglecalculation)
print(angles)
        
        #return angles #should be a tuple of 6 servo angles between 150 and 280 (a0,a1...,a5)
