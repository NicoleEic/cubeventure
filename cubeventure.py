import argparse
import numpy as np
import os
import sys
from time import sleep
import pandas as pd

# running on Mac for testing
if 'darwin' in sys.platform:
    from fake_rpi.RPi import GPIO as GPIO
    import matplotlib.pyplot as plt
    import mpl_toolkits.mplot3d.axes3d as p3
    from matplotlib import animation
    import matplotlib
    matplotlib.use("TkAgg")
# running on raspberry pi    
elif 'linux' in sys.platform:
    import RPi.GPIO as GPIO


def my_parser():
    parser = argparse.ArgumentParser(description='Optional description')
    if 'darwin' in sys.platform:
        vis_type = 'plot'
    elif 'linux' in sys.platform:
        vis_type = 'cube'
    parser.add_argument('--fname', type=str, help='path to visualization file', default='sequence')
    parser.add_argument('--matrix', type=np.array, help='numpy array with matrix', default=np.zeros(0))
    parser.add_argument('--pin_delay', type=np.float64, help='delay between pin outputs', default=0.0002)
    parser.add_argument('--time_step', type=np.float64, help='time between volumes in s', default=0.5)
    parser.add_argument('--cube_size', type=np.int, help='size of cube', default=3)
    parser.add_argument('--vis_type', type=str, help='cube, plot, plot_binary', default=vis_type)
    parser.add_argument('--n_steps_pin', type=np.int32, help='length of binary vetor', default=6)
    return parser


defaults = pd.DataFrame(columns=['bt_no', 'vis_name', 'time_step'])
defaults.loc[len(defaults)] = ['1', 'sequence', 0.1]
defaults.loc[len(defaults)] = ['2', 'rain', 0.5]
defaults.loc[len(defaults)] = ['3', 'sphere', 0.5]
defaults.loc[len(defaults)] = ['4', 'fillup', 0.5]
defaults.loc[len(defaults)] = ['5', 'intensity', 0.5]
defaults.loc[len(defaults)] = ['6', 'wave', 0.5]


def args_to_cmd(args):
    cmd_str = ""
    for arg in vars(args):
        cmd_str = cmd_str + f' --{arg} {getattr(args, arg)}'
    return cmd_str


# load 4d matrix from file
def load_matrix(fname):
    dd = os.path.join(os.path.dirname(__file__), 'sequences')
    # dd = '/home/pi/myCode/cubeventure/sequences'
    fpath = os.path.join(dd, fname) + '.npy'
    data_in = np.load(fpath)
    return data_in


def save_matrix(matrix, fname):
    dd = os.path.join(os.path.dirname(__file__), 'sequences')
    if not os.path.exists(dd):
        os.makedirs(dd)
    fname = os.path.join(dd, fname)
    if np.all((matrix == 1) | (matrix == 0)):
        matrix = matrix.astype(np.int32)
    np.save(fname, matrix)


def grid_array(i_grid):
    if i_grid == 3:
        col_pins = np.array([[13, 6, 4],
                       [22, 16, 27],
                       [5, 17, 26]])
        # top - middle - top
        ly_pins = [24, 23, 25]
    elif i_grid == 7:
        # TODO: check with Liam
        col_pins = np.array([[47, 39, 25, 26, 20, 22, 9],
                           [46, 38, 27, 28, 21, 23, 10],
                           [30, 29, 17, 18, 7, 11, 12],
                           [34, 36, 37, 42, 24, 15, 14],
                           [43, 44, 35, 0, 41, 16, 13],
                           [40, 32, 45, 19, 5, 8, 3],
                           [48, 33, 31, 6, 4, 2, 1]])
        ly_pins = [0, 2, 5, 3, 1, 4, 6]
    return col_pins, ly_pins


def intensity_to_binary(matrix, n_steps_pin):
    i_grid = matrix.shape[0]
    if matrix.ndim == 3:
        matrix = np.expand_dims(matrix, axis=4)
    t_steps = matrix.shape[3]    
    expanded = np.zeros((i_grid, i_grid, i_grid, n_steps_pin*t_steps))
    matrix = np.log10(matrix + 1)
    matrix = matrix / np.max(matrix)
    for i_t in np.arange(0, t_steps):
        vol = matrix[:, :, :, i_t]
        ind_start = i_t * n_steps_pin
        ind_stop = i_t * n_steps_pin + n_steps_pin
        # loop over z, x, y
        for iz in np.arange(0, i_grid):
            for ix in np.arange(0, i_grid):
                for iy in np.arange(0, i_grid):
                    intensity = vol[ix, iy, iz]
                    # convert intensity to binary vector
                    vec = np.zeros(n_steps_pin)
                    if intensity != 0:
                        step = np.round(1 / intensity).astype(np.int32)
                        vec[0::step] = 1
                    expanded[ix, iy, iz, ind_start:ind_stop] = vec
    return expanded


class Visualization:
    def __init__(self, args=my_parser().parse_known_args()[0], **kwargs):
        self.args = args
        self.ani_running = False
        if self.args.matrix.size < 2:
            self.matrix = load_matrix(self.args.fname)
        # use matrix directly
        else:
            self.matrix = self.args.matrix
        self.i_grid = self.matrix.shape[0]

    def start_stop(self):
        print('no start-stop possible')

    def close_animation(self):
        print('nothing to close')


class CubeRun(Visualization):
    def __init__(self, args, root, **kwargs):
        super(CubeRun, self).__init__(args)
        self.n_reps = np.ceil(self.args.time_step / (self.i_grid * self.args.pin_delay)).astype(np.int)
        self.root = root
        self.col_pins, self.ly_pins = grid_array(self.i_grid)
        self.i_v = 0
        try:
            self.setup_columns()
            #self.single_pin(col=5, layer=23)
        except:
            self.close_animation()
    
    def close_animation(self):
        self.ani_running = False
        GPIO.cleanup()
        print('closed')
        
    def start_stop(self):
        if self.ani_running:
            self.ani_running = False
        else:
            self.ani_running = True

    # initialisation of the pins
    def setup_columns(self):
        # GPIO pin addressing will use the virtual number
        GPIO.setmode(GPIO.BCM)
        # Initialise the pins so we can output values to them
        GPIO.setup(self.col_pins.reshape(-1).tolist(), GPIO.OUT)
        GPIO.setup(self.ly_pins, GPIO.OUT)
        GPIO.output(self.col_pins.reshape(-1).tolist(), False)
        GPIO.output(self.ly_pins, False)

    def update_time_step(self, time_step):
        setattr(self.args, 'time_step', time_step)
        self.n_reps = np.ceil(self.args.time_step / (self.args.n_steps_pin * self.i_grid * self.args.pin_delay)).astype(np.int)

    # function to turn on a single pin
    def single_pin(self, col=13, layer=23, t_light=5):
        GPIO.output(col, True)
        GPIO.output(layer, True)
        sleep(t_light)
        GPIO.output(col, False)
        GPIO.output(layer, False)

    def run_animation(self):
        self.ani_running = True
        if self.matrix.dtype != np.int32:
            print('convert intensities')
            # repetition of cycles through layers
            self.n_reps = np.ceil(self.args.time_step / (self.args.n_steps_pin * self.i_grid * self.args.pin_delay)).astype(np.int)
            self.run_expanded_vols()
        else:
            self.run_normal_vols()

    def run_expanded_vols(self):
        # loop over real volumes
        while self.i_v < self.matrix.shape[3]:
            if self.ani_running:
                vol = self.matrix[:, :, :, self.i_v]
                # convert intensities to binary matrix
                vol_exp = intensity_to_binary(vol, self.args.n_steps_pin)
                # loop over repetitions
                for _ in np.arange(0, self.n_reps):
                    # loop over expanded volumes
                    for i_s in np.arange(0, self.args.n_steps_pin):
                        vol_s = vol_exp[:, :, :, i_s]
                        self.show_vol(vol_s)
                        self.i_v = self.i_v + 1
                        self.root.update()
            else:
                self.root.update()

    def run_normal_vols(self):
        while self.i_v < self.matrix.shape[3]:
            if self.ani_running:
                vol = self.matrix[:, :, :, self.i_v]
                # loop over repetitions
                for _ in np.arange(0, self.n_reps):
                    self.show_vol(vol)
                self.i_v = self.i_v + 1
                self.root.update()
            else:
                self.root.update()

    def show_vol(self, vol):
        # loop over layers
        for i_z in np.arange(0, self.i_grid):
            # select active columns
            pins = self.col_pins[np.where(vol[:, :, i_z] != 0)].tolist()
            GPIO.output(pins, True)
            GPIO.output(self.ly_pins[i_z], True)
            sleep(self.args.pin_delay)
            GPIO.output(pins, False)
            GPIO.output(self.ly_pins[i_z], False)


class PlotRun(Visualization):
    def __init__(self, args, **kwargs):
        super(PlotRun, self).__init__(args)
        if self.args.vis_type == 'plot_binary':
            self.matrix = intensity_to_binary(self.matrix, self.args.n_steps_pin)
            self.update_rate = self.args.pin_delay * 1000
        else:
            self.update_rate = self.args.time_step * 1000

        # initialize figure
        self.x, self.y, self.z = np.meshgrid(np.arange(self.i_grid), np.arange(self.i_grid), np.arange(self.i_grid))
        self.fig = plt.figure()
        self.ax = p3.Axes3D(self.fig)
        self.ani = []
        self.fig.canvas.mpl_connect('button_press_event', self.start_stop)
        self.fig.canvas.mpl_connect('close_event', self.close_animation)
        if self.i_grid == 3:
            self.marker_size = 500
        elif self.i_grid == 7:
            self.marker_size = 50
        else:
            self.marker_size = 40

    def show_vol(self, vol):
        # TODO: how to change colours rather than redrawing plot?
        plt.cla()
        scat = self.ax.scatter(self.x.flatten(), self.y.flatten(), self.z.flatten(), s=self.marker_size, c=vol.reshape(-1), cmap='binary', depthshade=False, vmin=0, vmax=1, edgecolors="white")
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
        self.show_vol(data_vol)

    def update_time_step(self, time_step):
        self.ani.event_source.interval = time_step * 1000
        self.update_rate = time_step * 1000

    def start_stop(self, *event):
        if self.ani_running:
            self.ani.event_source.stop()
            self.ani_running = False
        else:
            self.ani.event_source.start()
            self.ani_running = True

    def close_animation(self, *event):
        if self.ani.event_source:
            self.ani.event_source.stop()
        self.ani_running = False
        plt.close('all')

    def run_animation(self):
        self.ani_running = True
        # animation for 4D matrix
        if len(self.matrix.shape) == 4:
            self.ani = animation.FuncAnimation(self.fig, self.update_plot, interval=self.update_rate, frames=self.matrix.shape[3])
            plt.show()
        # static plot if only 3D matrix
        elif len(self.matrix.shape) == 3:
            plt.cla()
            self.show_vol(self.matrix)
