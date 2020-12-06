import numpy as np
import cubeventure as cv
import os

i_grid = 3
n_intensity_steps = 6

matrix = np.ones((i_grid, i_grid, i_grid, n_intensity_steps + 1))
for i, ind in enumerate(np.linspace(1, 0, n_intensity_steps)):
	matrix[:,:,:,i+1] = ind
	
matrix = np.append(matrix, np.flip(matrix, axis=3), axis=3)
matrix = np.append(matrix, matrix, axis=3)


cv.save_matrix(matrix, 'test')
os.system("python3 run_visualisation.py --fname test --vis_type cube --time_step 0.3")






