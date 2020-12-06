import numpy as np
import os
import scipy.ndimage.interpolation

i_grid = 7
space = 3
n_steps = 100
# initialize output matrix
data_matrix = np.zeros((i_grid, i_grid, i_grid, n_steps))

plane = np.eye(i_grid) + np.eye(i_grid, k=space) + np.eye(i_grid, k=-space)

for i in np.arange(0, n_steps):
    plane = np.insert(plane, 0, plane[-1, :], axis=0)[:-1, :]
    data_matrix[:, :, :, i] = np.repeat(plane[:, :, np.newaxis], i_grid, axis=2)







### save matrix
# data path
dd = os.path.join(os.path.dirname(__file__), 'sequences')
# output filename
fname = os.path.join(dd, 'plane')
np.save(fname, data_matrix)

# call visualization script
os.system("python visualisation_demo.py plane")