import numpy as np
import cubeventure as cv
import os

i_grid = 3
mx = np.zeros((i_grid, i_grid, i_grid, 100))
t = np.arange(0, mx.shape[3]+i_grid*2)
bins = np.arange(0, i_grid+1)
centers = (bins[1:] + bins[:-1]) / 2
z_arr = bins[np.digitize(np.sin(t/2)*(i_grid+1)/2+(i_grid+1)/2, centers)]

for ix in np.arange(0, i_grid):
    for iy in np.arange(0, i_grid):
        for it in np.arange(0, mx.shape[3]):
            z = z_arr[it+ix]
            mx[ix, iy, 0:z, it] = 1

fname = 'wave'
cv.save_matrix(mx, fname)
# call visualization script
os.system(f"python run_visualisation.py --fname {fname} --vis_type plot --time_step 0.1")

