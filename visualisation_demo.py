from matplotlib import pyplot as plt
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation
import matplotlib
matplotlib.use("TkAgg")


def main():
    i_grid = 7
    t_step = 200 # milliseconds
    x, y, z = np.meshgrid(np.arange(i_grid), np.arange(i_grid), np.arange(i_grid))
    fig = plt.figure()
    ax = p3.Axes3D(fig)

    n_vols = i_grid**3
    data_in = np.zeros((i_grid, i_grid, i_grid, n_vols))
    i_all = 0
    for i_x in np.arange(i_grid):
        for i_y in np.arange(i_grid):
            for i_z in np.arange(i_grid):
                data_in[:, :, :, i_all] = 0
                data_in[i_x, i_y, i_z, i_all] = 1
                i_all = i_all + 1

    def update_plot(i):
        data_vol = data_in[:, :, :, i]
        # TODO: how to change colours rather than redrawing plot?
        plt.cla()
        scat = ax.scatter(x.flatten(), y.flatten(), z.flatten(), c=data_vol.reshape(-1), cmap='binary',
                          depthshade=False, vmin=0, vmax=1, edgecolors="black")

        ax.set_xticklabels("")
        ax.set_yticklabels("")
        ax.set_zticklabels("")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        return scat,

    ani = animation.FuncAnimation(fig, update_plot, interval=t_step, frames=data_in.shape[3])
    plt.show()


main()
