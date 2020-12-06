import numpy as np
import cubeventure as cv
import os


i_grid = 3
matrix = np.ones((i_grid, i_grid, i_grid, 5))
matrix[:,:,:,1] = 0.5
matrix[:,:,:,2] = 0
matrix[:,:,:,3] = 0.2
matrix[:,:,:,4] = 1
matrix = np.append(matrix, matrix, axis=3)

cv.save_matrix(matrix, 'test')
os.system("python3 run_visualisation.py --fname test --vis_type plot_binary --time_step 1")






