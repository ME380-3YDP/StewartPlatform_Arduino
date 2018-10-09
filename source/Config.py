import numpy as np
mechParams={
    'radius':0.5,
    'upperPlatformScale': 2.0/3.0,
    'midZHeight': np.array([0, 0, 0.4]), # height of the platform taken as the Z=0 reference
    'defaultLength': 0.1, # length of the syringe assembly when the syringe is fully retracted
}
options={
    'transformMode': "quaternion"  # select which transformation method we are using
}
