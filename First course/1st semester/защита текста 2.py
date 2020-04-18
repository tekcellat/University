import numpy as np
 
arr = np.array([1, 1, 4, 4, 4, 4, 2, 2, 2, 20, 20, 20, 13, 9])
arru = np.unique(arr)
 
freq0 = arr == arru[:, np.newaxis]
freq = np.sum(freq0, axis=1)
print arru[freq > 1]
