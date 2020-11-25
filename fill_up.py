import numpy as np
import os

i_grid = 7

data_matrix = np.zeros((i_grid, i_grid, i_grid, i_grid**3))


for i in np.arange(0, i_grid**3):
    long = data_matrix[:, :, :, 0].reshape(i_grid ** 3)
    ind = np.random.choice(np.where(long == 0)[0])
    long[ind] = 1
    back = long.reshape(i_grid, i_grid, i_grid)
    data_matrix[:, :, :, i] = back

### save matrix
# data path
dd = os.path.join(os.path.dirname(__file__), 'sequences')
# output filename
fname = os.path.join(dd, 'fill_up')
np.save(fname, data_matrix)

# call visualization script
os.system("python visualisation_demo.py fill_up")