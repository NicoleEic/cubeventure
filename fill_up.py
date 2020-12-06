import numpy as np
import os

i_grid = 3

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

### save matrix
# data path
dd = os.path.join(os.path.dirname(__file__), 'sequences')
if not os.path.exists(dd):
    os.makedirs(dd)

# output filename
fname = os.path.join(dd, 'fill_up')
np.save(fname, data_matrix)

# call visualization script
os.system("python run_visualisation.py --fname fill_up --time_step=0.1")
