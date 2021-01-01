import numpy as np
import os
import cubeventure as cv

visu_name = 'fillup'
i_grid = 7

data_matrix = np.zeros((i_grid, i_grid, i_grid, i_grid**3))

for i in np.arange(1, i_grid**3):
    long = data_matrix[:, :, :, 0].reshape(i_grid ** 3)
    ind = np.random.choice(np.where(long == 0)[0])
    long[ind] = 1
    back = long.reshape(i_grid, i_grid, i_grid)
    data_matrix[:, :, :, i] = back

# TODO: why does the first volume appear as all lights on?
# crop out as solution for now
data_matrix = data_matrix[:, :, :, 1:-1]

cv.save_matrix(data_matrix, visu_name)

# call visualization script
os.system(f'python run_visualisation.py --fname {visu_name} --vis_type plot --time_step 0.5')

