import numpy as np
import os
import cubeventure as cv

visu_name = 'plane'
i_grid = 7
space = 3
n_steps = 100
# initialize output matrix
data_matrix = np.zeros((i_grid, i_grid, i_grid, n_steps))

plane = np.eye(i_grid) + np.eye(i_grid, k=space) + np.eye(i_grid, k=-space)

for i in np.arange(0, n_steps):
    plane = np.insert(plane, 0, plane[-1, :], axis=0)[:-1, :]
    data_matrix[:, :, :, i] = np.repeat(plane[:, :, np.newaxis], i_grid, axis=2)


cv.save_matrix(data_matrix, visu_name)

# call visualization script
os.system(f'python run_visualisation.py --fname {visu_name} --vis_type plot --time_step 0.3')