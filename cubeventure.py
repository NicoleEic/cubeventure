import argparse
import numpy as np
import os

def my_parser():
    parser = argparse.ArgumentParser(description='Optional description')
    parser.add_argument('--fname', type=str, help='path to visualization file', default='sequence')
    parser.add_argument('--matrix', type=np.array, help='numpy array with matrix', default=np.zeros(0))
    parser.add_argument('--pin_delay', type=np.float64, help='delay between pin outputs', default=0.001)
    parser.add_argument('--time_step', type=np.float64, help='time between volumes in s', default=0.5)
    parser.add_argument('--cube_size', type=np.int, help='size of cube', default=3)
    parser.add_argument('--vis_type', type=str, help='cube, plot, plot_binary', default='plot')
    parser.add_argument('--pin_reps', type=np.int32, help='length of binary vetor', default=6)
    return parser


def args_to_cmd(args):
    cmd_str = ""
    for arg in vars(args):
        cmd_str = cmd_str + f' --{arg} {getattr(args, arg)}'
    return cmd_str


# load 4d matrix from file
def load_data(fname):
    dd = os.path.join(os.path.dirname(__file__), 'sequences')
    # dd = '/home/pi/myCode/cubeventure/sequences'
    fpath = os.path.join(dd, fname) + '.npy'
    data_in = np.load(fpath)
    return data_in


def save_matrix(matrix, fname):
    dd = os.path.join(os.path.dirname(__file__), 'sequences')
    fname = os.path.join(dd, fname)
    np.save(fname, matrix)


def grid_array(i_grid):
    if i_grid == 3:
        col_pins = np.array([[13, 6, 4],
                       [22, 16, 27],
                       [5, 17, 26]])
        # top - middle - top
        ly_pins = [25, 24, 23]
    elif i_grid == 7:
        print('define pin array')
    return col_pins, ly_pins


def intensity_to_binary(matrix, n_steps_pin):
    i_grid = matrix.shape[0]
    t_steps = matrix.shape[3]
    expanded = np.zeros((i_grid, i_grid, i_grid, n_steps_pin*t_steps))
    for i_t in np.arange(0, t_steps):
        vol = matrix[:, :, :, i_t]
        ind_start = i_t * n_steps_pin
        ind_stop = i_t * n_steps_pin + n_steps_pin
        # loop over z
        for iz in np.arange(0, i_grid):
            # loop over x
            for ix in np.arange(0, i_grid):
                # loop over z
                for iy in np.arange(0, i_grid):
                    # convert intensity to binary vector
                    intensity = vol[ix, iy, iz]
                    vec = np.zeros(n_steps_pin)
                    if intensity != 0:
                        step = np.round(1 / intensity).astype(np.int32)
                        vec[0::step] = 1
                    expanded[ix, iy, iz, ind_start:ind_stop] = vec
    return expanded
