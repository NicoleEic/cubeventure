from matplotlib import pyplot as plt
import os
import sys
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation
import matplotlib
matplotlib.use("TkAgg")


def main():

    # load 4d matrix from file
    dd = os.path.join(os.path.dirname(__file__), 'sequences')
    # default sequence
    if len(sys.argv) == 1:
        fname = os.path.join(dd, 'sequence') + '.npy'
    # if command line argument provided
    else:
        fname = os.path.join(dd, sys.argv[1]) + '.npy'
        if not os.path.isfile(fname):
            print('sequence does not exist')
    data_in = np.load(fname)

    i_grid = data_in.shape[0]
    t_step = 200 # milliseconds

    # initialize 3D scatter plot
    x, y, z = np.meshgrid(np.arange(i_grid), np.arange(i_grid), np.arange(i_grid))
    fig = plt.figure()
    ax = p3.Axes3D(fig)



    def update_plot(i):
        # read in each slice of the 4D matrix
        data_vol = data_in[:, :, :, i]
        # TODO: how to change colours rather than redrawing plot?
        plt.cla()
        scat = ax.scatter(x.flatten(), y.flatten(), z.flatten(), c=data_vol.reshape(-1), cmap='binary',
                          depthshade=False, vmin=0, vmax=1, edgecolors="white")

        ax.set_xticklabels("")
        ax.set_yticklabels("")
        ax.set_zticklabels("")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        return scat,

    # create visualization
    # animation for 4D matrix
    if len(data_in.shape) == 4:
        ani = animation.FuncAnimation(fig, update_plot, interval=t_step, frames=data_in.shape[3])
        plt.show()
    # static plot if only 3D matrix
    elif len(data_in.shape) == 3:
        plt.cla()
        scat = ax.scatter(x.flatten(), y.flatten(), z.flatten(), c=data_in.reshape(-1), cmap='binary',
                          depthshade=False, vmin=0, vmax=1, edgecolors="white")
        ax.set_xticklabels("")
        ax.set_yticklabels("")
        ax.set_zticklabels("")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()


main()
