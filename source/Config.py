import numpy as np
mechParams={
    'radius':0.100,
    'scale': .55,# ratio of top to bottom platform radius
    'defaultLength': 0.227,   # length of the syringe assembly when the syringe is fully retracted
    'rangeOfMotion': 0.030,
    'crankLength': 0.017, # length of crank from servo center to the pivot
    "conRodLength": 0.074,  # length of con rod, (center to center distance)
}
options={
    'transformMode': "normal"  # select which transformation method we are using
}
