#def computeAangles(self, length):
        #input tuple of 6 lengths of the form (L0,L1,L2,L3,L4,L5) in mm defined as positive from the fully retracted position of the syringe.
import numpy as np
import math
import array

length = [1, 2, 3, 4, 5, 6]#to be removed once code is complete
angles=[]
a = 0.035 #length of crank, subject to change
b = 0.0075 #length of con rod, subject to change
c = [a+b, a+b, a+b, a+b, a+b, a+b] #starting length when syringe plunger fully enclosed (retracted pos'n)
print(length)
c_length =[]
c_length =np.subtract(c, length) #so we can use trig functions
print(c_length)
inverseanglemath=np.array
inverseangle=[]
anglecalculation=[]
for i in range(6):
    inverseanglemath=(-(b**2 - a**2 - (c_length)**2)/(2*a*c_length))
    inverseangle.append(inverseanglemath)
    print(inverseangle)
    for j in range (6):
        anglecalculation=math.acos(inverseangle)
        angles.append(anglecalculation)
print(angles)
        
        #return angles #should be a tuple of 6 servo angles between 150 and 280 (a0,a1...,a5)
