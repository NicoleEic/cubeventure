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

# repetition of cycles through layers
# TODO: change sampling frequency in case it does not fit
n_reps = np.int(t_s / t_p)


# load 4d matrix from file
fname = args.fname
dd = os.path.join(os.path.dirname(__file__), 'sequences')
#dd = '/home/pi/myCode/cubeventure/sequences'
fpath = os.path.join(dd, fname) + '.npy'
data_in = np.load(fpath)


# initialisation of the pins 
def setupColumns():
    # GPIO pin addressing will use the virtual number
    GPIO.setmode(GPIO.BCM)
    # Initialise the pins so we can output values to them 
    GPIO.setup(pa.reshape(-1).tolist(), GPIO.OUT)
    GPIO.setup(layers, GPIO.OUT)
    GPIO.output(pa.reshape(-1).tolist(), False)
    GPIO.output(layers, False)
    
    
def test():
    GPIO.output(17, True)
    GPIO.output(23, True)
    sleep(5)
    GPIO.output(17, False)
    GPIO.output(23, False)
    

def show_pattern(pattern):
    for i_v in np.arange(0, data_in.shape[3]):
        vol = data_in[:,:,:,i_v]
        for i_r in np.arange(0, n_reps):
            for layer in np.arange(0, i_grid):
                pins = pa[np.where(vol[:,:,layer] !=0)].tolist()
                GPIO.output(pins, True)
                GPIO.output(layers[layer], True)
                sleep(t_p)
                GPIO.output(pins, False)
                GPIO.output(layers[layer], False)

# mainline logic 
try:
    print('Press CTRL+C to stop script')
    setupColumns()
    show_pattern(data_in)
    #test()
 
except KeyboardInterrupt:
    GPIO.cleanup()

finally:
    GPIO.cleanup()
