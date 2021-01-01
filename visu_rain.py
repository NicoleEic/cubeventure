import numpy as np
import os
import cubeventure as cv

visu_name = 'rain'
i_grid = 7
n_drops = 50
vols_max = 50

# initialize matrix
data_matrix = np.zeros((i_grid, i_grid, i_grid, vols_max))

# define a falling drop
drop_column = np.zeros((1, 1, i_grid, i_grid))
for i in np.arange(0, i_grid):
    drop_column[0, 0, i_grid-1-i, i] = 1

# chose random start points for drops
for d in np.arange(0, n_drops):
    x_d = np.random.choice(np.arange(0, i_grid))
    y_d = np.random.choice(np.arange(0, i_grid))
    t_d = np.random.choice(np.arange(0, vols_max - i_grid))
    data_matrix[x_d, y_d, :, t_d:t_d+i_grid] = data_matrix[x_d, y_d, :, t_d:t_d+i_grid] + drop_column

# add ceiling
data_matrix[:, :, i_grid-1, :] = 1

# crop un-used volumes
final_vol = np.max(np.nonzero(data_matrix.reshape(-1, data_matrix.shape[-1])))
data_matrix = data_matrix[:, :, :, 0:final_vol]

cv.save_matrix(data_matrix, visu_name)

# call visualization script
os.system(f'python run_visualisation.py --fname {visu_name} --vis_type plot --time_step 0.3')
