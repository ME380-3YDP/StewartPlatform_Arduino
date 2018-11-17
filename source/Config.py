import numpy as np
mechParams={
    'radius':0.100,
    'scale': 2.0/3.0,# ratio of top to bottom platform radius
    'defaultLength': 0.15,   # length of the syringe assembly when the syringe is fully retracted
    'rangeOfMotion': 0.058,
    'crankLength': 0.049, # length of crank. This is measured with the hole spacing center to center (last clearance hole to the hole that connects to the conrod)
    "conRodLength": 0.0625,  # length of con rod, (center to center distance)
}
options={
    'transformMode': "normal"  # select which transformation method we are using
}
