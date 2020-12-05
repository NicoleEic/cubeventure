from matplotlib import pyplot as plt
import cubeventure
import time
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation
import matplotlib
matplotlib.use("TkAgg")


class PlotSequence:
    def __init__(self):
        self.args = cubeventure.my_parser().parse_args()
        print(self.args)
        if len(self.args.matrix) == 0:
            self.matrix = cubeventure.load_data(self.args.fname)
        else:
            self.matrix = self.args.matrix
        self.i_grid = self.matrix.shape[0]
        self.x, self.y, self.z = np.meshgrid(np.arange(self.i_grid), np.arange(self.i_grid), np.arange(self.i_grid))
        self.fig = plt.figure()
        self.ax = p3.Axes3D(self.fig)
        self.run_animation()

    def plot_volume(self, vol):
        # TODO: how to change colours rather than redrawing plot?
        plt.cla()
        scat = self.ax.scatter(self.x.flatten(), self.y.flatten(), self.z.flatten(), c=vol.reshape(-1), cmap='binary', depthshade=False, vmin=0, vmax=1, edgecolors="white")
        self.ax.set_xticklabels("")
        self.ax.set_yticklabels("")
        self.ax.set_zticklabels("")
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        return scat

    def update_plot(self, i):
        # read in each volume of the 4D matrix
        data_vol = self.matrix[:, :, :, i]
        self.plot_volume(data_vol)

    def run_animation(self):
        # animation for 4D matrix
        if len(self.matrix.shape) == 4:
            ani = animation.FuncAnimation(self.fig, self.update_plot, interval=self.args.time_step*1000, frames=self.matrix.shape[3])
            plt.show()
        # static plot if only 3D matrix
        elif len(self.matrix.shape) == 3:
            plt.cla()
            self.plot_volume(self.matrix)


if __name__ == "__main__":
    my_plot = PlotSequence()


