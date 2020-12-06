import numpy as np
import cubeventure as cv
import os

matrix = np.ones((7, 7, 7, 5))
matrix[:,:,:,1] = 0.5
matrix[:,:,:,2] = 0
matrix[:,:,:,3] = 0.5
matrix[:,:,:,4] = 1

cv.save_matrix(matrix, 'test')
os.system("python run_visualisation.py --fname test --vis_type plot_binary --time_step 0.5")






