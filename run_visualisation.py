import RPi.GPIO as GPIO 
from time import sleep
import numpy as np
import os
import sys
import argparse

parser = argparse.ArgumentParser(description='Optional description')
parser.add_argument('--fname', type=str, help='path to visualization file', default='fill_up')
parser.add_argument('--pin_delay', type=np.float64, help='delay between pin outputs', default=0.001)
parser.add_argument('--time_step', type=np.float64, help='time between volumes', default=0.5)
parser.add_argument('--cube_size', type=np.int, help='size of cube', default=3)
args = parser.parse_args()

print(args)

i_grid = args.cube_size

# array of pins for columns
if i_grid == 3:
    pa = np.array([[13, 6, 4],
                   [22, 16, 27],
                   [5, 17, 26]])
    # top - middle - top
    layers = [25, 24, 23]
elif i_grid == 7:
    print('define pin array')
    sys.exit()
        

# Time delay built in between pin output
t_p = args.pin_delay

# time step between volumes (needs to be multiples of t_p)
t_s = args.time_step


# number of alterations to code for intensity
n_steps_pin = 6

# repetition of cycles through layers
n_reps_layer = np.ceil(t_s / (n_steps_pin * i_grid * t_p)).astype(np.int)


# load 4d matrix from file
def read_in_data(fname):
    fname = args.fname
    dd = os.path.join(os.path.dirname(__file__), 'sequences')
    #dd = '/home/pi/myCode/cubeventure/sequences'
    fpath = os.path.join(dd, fname) + '.npy'
    data_in = np.load(fpath)
    return data_in


# initialisation of the pins 
def setupColumns():
    # GPIO pin addressing will use the virtual number
    GPIO.setmode(GPIO.BCM)
    # Initialise the pins so we can output values to them 
    GPIO.setup(pa.reshape(-1).tolist(), GPIO.OUT)
    GPIO.setup(layers, GPIO.OUT)
    GPIO.output(pa.reshape(-1).tolist(), False)
    GPIO.output(layers, False)
    

# function to turn on a single pin
def single_pin(col, layer):
    GPIO.output(col, True)
    GPIO.output(layer, True)
    sleep(5)
    GPIO.output(col, False)
    GPIO.output(layer, False)


def intensity_to_binary(vol):
    expanded = np.zeros((i_grid, i_grid, i_grid, n_steps_pin))
    for i_r in np.arange(0, n_reps_layer):
        for iz in np.arange(0, i_grid):
            # loop over x and z
            for ix in np.arange(0, vol.shape[0]):
                for iy in np.arange(0, vol.shape[1]):
                    # convert intensity to binary vector
                    intensity = vol[ix, iy, iz]
                    vec = np.zeros(n_steps_pin)
                    if intensity != 0:
                        step = np.round(1 / intensity).astype(np.int)
                        vec[0::step] = 1
                    expanded[ix, iy, iz, :] = vec
    return expanded


def show_pattern(pattern):
    # loop over time points in matrix
    for i_t in np.arange(0, data_in.shape[3]):
        # extract single volume
        vol = data_in[:, :, :, i_t]
        # convert intensity values in volume to 4D binary matrix
        vol_exp = intensity_to_binary(vol)
        # loop over elements of expanded matrix
        for i_v in np.arange(0, n_steps_pin):
            # extract sincle time point volume
            vol_step = vol_exp[:, :, :, i_v]
            # loop over repetitions
            for i_r in np.arange(0, n_reps_layer):
                # loop over layers
                for i_z in np.arange(0, i_grid):
                    # select active columns
                    pins = pa[np.where(vol[:, :, i_z] != 0)].tolist()
                    GPIO.output(pins, True)
                    GPIO.output(layers[i_z], True)
                    sleep(t_p)
                    GPIO.output(pins, False)
                    GPIO.output(layers[i_z], False)

# Mainline logic . . . 
try:
    print('Press CTRL+C to stop script')
    setupColumns()
    data_in = read_in_data(args.fname)
    show_pattern(data_in)

except KeyboardInterrupt:
    GPIO.cleanup()

finally:
    GPIO.cleanup()
