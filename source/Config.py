import numpy as np
mechParams={
    'radius':0.5,
    'upperPlatformScale': 2.0/3.0,
    'lowestZ':np.array([0, 0, 0.3]),  # zero point for Z-translations
}
options={
    'transformMode': "quaternion"  # select which transformation method we are using
}
