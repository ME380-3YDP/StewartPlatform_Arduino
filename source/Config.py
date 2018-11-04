import numpy as np
mechParams={
    'radius':0.1,
    'scale': 2.0/3.0,# ratio of top to bottom platform radius
    'midZHeight': np.array([0, 0, 0.4]), # height of the platform taken as the Z=0 reference
    'defaultLength': 0.12,   # length of the syringe assembly when the syringe is fully retracted
    'rangeOfMotion':0.058,
}
options={
    'transformMode': "normal"  # select which transformation method we are using
}
