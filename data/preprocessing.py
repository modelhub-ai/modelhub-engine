# preprocess.py
# preprocesses numpy arrays according to contributors' pipeline
import numpy as np

def preprocess(arr):
    if arr.shape[1] > 3:
        arr = arr[:,0:3,:,:]
    elif arr.shape[1] < 3:
        arr = arr[:,[0],:,:]
        arr = np.concatenate((arr, arr[:,[0],:,:]), axis = 1)
        arr = np.concatenate((arr, arr[:,[0],:,:]), axis = 1)
    print ('preprocessing done.')
    return arr
