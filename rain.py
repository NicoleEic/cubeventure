import numpy as np
import random
import os

i_grid = 7

n_drops = 200
vols_max = 100

# initialize matrix
data_matrix = np.zeros((i_grid, i_grid, i_grid, vols_max))

# define a falling drop
drop_column = np.zeros((1, 1, i_grid, i_grid))
for i in np.arange(0, i_grid):
    drop_column[0, 0, 6-i, i] = 1

# chose random start points for drops
for d in np.arange(0, n_drops):
    x_d = np.random.choice(np.arange(0, i_grid))
    y_d = np.random.choice(np.arange(0, i_grid))
    t_d = np.random.choice(np.arange(0, vols_max - 7))
    data_matrix[x_d, y_d, :, t_d:t_d+7] = data_matrix[x_d, y_d, :, t_d:t_d+7] + drop_column

# add ceiling
data_matrix[:, :, 6, :] = 1

# crop un-used volumes
final_vol = np.max(np.nonzero(data_matrix.reshape(-1, data_matrix.shape[-1])))
data_matrix = data_matrix[:, :, :, 0:final_vol]

### save matrix
# data path
dd = os.path.join(os.path.dirname(__file__), 'sequences')
# output filename
fname = os.path.join(dd, 'rain')
np.save(fname, data_matrix)

# call visualization script
os.system("python visualisation_demo.py rain")
