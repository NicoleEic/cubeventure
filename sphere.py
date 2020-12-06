import numpy as np
import os
import scipy.ndimage
import cubeventure as cv
from matplotlib import pyplot as plt

i_grid = 3

# initialize empty matrix with centre 1
data_matrix = np.zeros((i_grid, i_grid, i_grid))
data_matrix = data_matrix[..., np.newaxis]
vol = np.zeros((i_grid, i_grid, i_grid))
mid = np.int(np.floor(i_grid/2))
vol[mid, mid, mid] = 10

# create spheres with various radius
n_steps = 6
thres = 0.5
for sig in np.arange(0, n_steps):
    vol_s = scipy.ndimage.filters.gaussian_filter(vol, [sig, sig, sig], mode='constant')
    vol_s = vol_s / np.max(vol_s)
    #vol_s = np.where(vol_s > thres, 1, 0)
    # append 4D matrix
    data_matrix = np.append(data_matrix, vol_s[:, :, :, np.newaxis], axis=3)

# flip matrix for decreasing sphere
data_matrix = np.append(data_matrix, np.flip(data_matrix), axis=3)

cv.save_matrix(data_matrix, 'sphere')

# call visualization script
os.system("python run_visualisation.py --fname sphere --vis_type plot --time_step 0.2")

