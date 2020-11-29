import numpy as np
import os
import scipy.ndimage.interpolation

i_grid = 3
# number of rotating slices
n_slices = 10
# number of steps to interpolate for rotation
n_steps = 100
angles = np.linspace(10, 360, n_steps)
# possible rotation axes
axes = ((0, 1), (0, 2), (1, 2))
# initialize output matrix
data_matrix = np.zeros((i_grid, i_grid, i_grid, n_slices * n_steps))

i = 0
# loop over slices
for i_slice in np.arange(0, n_slices):
    # initialize empty volume
    vol = np.zeros((i_grid, i_grid, i_grid))
    # select one of the three start plates
    plane = np.random.choice([0, 1, 2])
    if plane == 0:
        # fill volume with plane of 1s
        vol[3, :, :] = 1
        # select one of the two rotation axes
        ax = axes[np.random.choice([0, 1])]
    elif plane == 1:
        vol[:, 3, :] = 1
        ax = axes[np.random.choice([0, 2])]
    elif plane == 2:
        vol[:, :, 3] = 1
        ax = axes[np.random.choice([1, 2])]

    # loop over each rotation angle
    for angle in angles:
        # rotate slice
        new = scipy.ndimage.interpolation.rotate(vol, angle, axes=ax, mode='nearest', order=1)
        # normalize and binarize
        new = new / np.max(new)
        new = np.where(new > 0.4, 1, 0)
        # select only inner cube of 7x7x7
        lows = np.floor(np.array(new.shape)/2).astype(np.int) - 3
        highs = lows + 7
        new = new[lows[0]:highs[0], lows[1]:highs[1], lows[2]:highs[2]]
        # append to data_matrix
        data_matrix[:, :, :, i] = new
        i = i+1

### save matrix
# data path
dd = os.path.join(os.path.dirname(__file__), 'sequences')
# output filename
fname = os.path.join(dd, 'slice')
np.save(fname, data_matrix)

# call visualization script
os.system("python visualisation_demo.py slice")
