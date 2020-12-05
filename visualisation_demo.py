from matplotlib import pyplot as plt
import cubeventure
import os
import sys
import argparse
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation
import matplotlib
matplotlib.use("TkAgg")

parser = cubeventure.my_parser()
args = parser.parse_args()
print(args)

if len(args.matrix) == 0:
    data_in = cubeventure.load_data(args.fname)
else:
    data_in = args.matrix

i_grid = data_in.shape[0]

# initialize 3D scatter plot
x, y, z = np.meshgrid(np.arange(i_grid), np.arange(i_grid), np.arange(i_grid))
fig = plt.figure()
ax = p3.Axes3D(fig)

def plot_volume(vol):
    # TODO: how to change colours rather than redrawing plot?
    plt.cla()
    scat = ax.scatter(x.flatten(), y.flatten(), z.flatten(), c=vol.reshape(-1), cmap='binary', depthshade=False, vmin=0, vmax=1, edgecolors="white")
    ax.set_xticklabels("")
    ax.set_yticklabels("")
    ax.set_zticklabels("")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    return scat


def update_plot(i):
    # read in each volume of the 4D matrix
    data_vol = data_in[:, :, :, i]
    plot_volume(data_vol)


# animation for 4D matrix
if len(data_in.shape) == 4:
    ani = animation.FuncAnimation(fig, update_plot, interval=args.time_step*1000, frames=data_in.shape[3])
    plt.show()
# static plot if only 3D matrix
elif len(data_in.shape) == 3:
    plt.cla()
    plot_volume(data_in)


