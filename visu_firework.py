import numpy as np
import os
import cubeventure as cv

visu_name = 'firework'
i_grid = 7
mid = np.floor(i_grid/2).astype(np.int)

data_matrix = np.zeros((i_grid, i_grid, i_grid, 30))

# define a falling drop
def make_drop_mat(mat, x, y, t):
    drop_mat = np.zeros((i_grid, i_grid, i_grid, i_grid))
    for i in np.arange(0, i_grid):
        drop_mat[x, y, i_grid-1-i, i] = 1
    mat[:, :, :, t:t+i_grid] = mat[:, :, :, t:t+i_grid] + drop_mat
    return mat

# 0
data_matrix[mid, mid, 0, 0] = 1
for i in [1 ,2, 3, 4]:
    data_matrix[:, :, :, i] = data_matrix[:, :, :, i-1]
    data_matrix[mid, mid, i, i] = 1

data_matrix[:, :, :, 5] = data_matrix[:, :, :, 4]
data_matrix[mid-1:mid+1, mid-1:mid+1, 5, 5] = 1

data_matrix[:, :, :, 6] = data_matrix[:, :, :, 5]
data_matrix[:, :, 6, 6] = 1

for i in np.arange(7, 14):
    data_matrix[:, :, :, i] = data_matrix[:, :, :, 6]

data_matrix[mid, mid, 0, 7:14] = 0
data_matrix[mid, mid, 1, 8:14] = 0
data_matrix[mid, mid, 2, 8:14] = 0
data_matrix[mid, mid, 3, 9:14] = 0
data_matrix[mid, mid, 4, 9:14] = 0
data_matrix[mid-1:mid+1, mid-1:mid+1, 5, 10:14] = 0
data_matrix[0::3, 0::3, 6, 10:14] = 0
data_matrix[0::2, 0::2, 6, 11:14] = 0


data_matrix = make_drop_mat(data_matrix, 0, 2, 7)
data_matrix = make_drop_mat(data_matrix, 0, 3, 8)
data_matrix = make_drop_mat(data_matrix, 0, 6, 7)
data_matrix = make_drop_mat(data_matrix, 6, 2, 8)
data_matrix = make_drop_mat(data_matrix, 6, 4, 9)

data_matrix = make_drop_mat(data_matrix, 2, 0, 7)
data_matrix = make_drop_mat(data_matrix, 3, 0, 8)
data_matrix = make_drop_mat(data_matrix, 6, 0, 9)
data_matrix = make_drop_mat(data_matrix, 2, 6, 8)
data_matrix = make_drop_mat(data_matrix, 4, 6, 7)

data_matrix = make_drop_mat(data_matrix, 2, 2, 8)


# crop un-used volumes
final_vol = np.max(np.nonzero(data_matrix.reshape(-1, data_matrix.shape[-1])))
data_matrix = data_matrix[:, :, :, 0:final_vol]

cv.save_matrix(data_matrix, visu_name)

# call visualization script
os.system(f'python visualization_wrapper.py --fname {visu_name} --vis_type plot --time_step 0.2')

