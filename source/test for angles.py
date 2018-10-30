#def computeAangles(self, length):
        #input tuple of 6 lengths of the form (L0,L1,L2,L3,L4,L5) in mm defined as positive from the fully retracted position of the syringe.
import numpy as np
import math

length = [0.003, 0.002, 0.003, 0.003, 0.003, 0.003] #to be removed with def and real shiz once code is complete
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
print(angles)
        
        #return angles #should be a tuple of 6 servo angles between 150 and 280 (a0,a1...,a5)
