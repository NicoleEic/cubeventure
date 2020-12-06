from time import sleep
import numpy as np
import os
import sys
import argparse
import cubeventure as cv


class CubeSequence:
    def __init__(self, args):
        try:
            self.args = args
            self.i_grid = args.cube_size
            self.col_pins, self.ly_pins = cv.grid_array(self.i_grid)
            # Time delay built in between pin output
            t_p = args.pin_delay
            # time step between volumes (needs to be multiples of t_p)
            t_s = args.time_step
            # number of alterations to code for intensity
            self.n_steps_pin = 6
            # repetition of cycles through layers
            self.n_reps_layer = np.ceil(t_s / (self.n_steps_pin * self.i_grid * t_p)).astype(np.int)
            if len(self.args.matrix) == 0:
                self.matrix = cv.load_data(self.args.fname)
            else:
                self.matrix = self.args.matrix
            self.setup_columns()
            self.show_pattern()
        except KeyboardInterrupt:
            GPIO.cleanup()
        finally:
            GPIO.cleanup()

    # initialisation of the pins
    def setup_columns(self):
        # GPIO pin addressing will use the virtual number
        GPIO.setmode(GPIO.BCM)
        # Initialise the pins so we can output values to them
        GPIO.setup(self.col_pins.reshape(-1).tolist(), GPIO.OUT)
        GPIO.setup(self.ly_pins, GPIO.OUT)
        GPIO.output(self.col_pins.reshape(-1).tolist(), False)
        GPIO.output(self.ly_pins, False)

    # function to turn on a single pin
    def single_pin(self, col, layer, t_light=5):
        GPIO.output(col, True)
        GPIO.output(layer, True)
        sleep(t_light)
        GPIO.output(col, False)
        GPIO.output(layer, False)

    def show_pattern(self):
        # convert intensity values in volume to 4D binary matrix
        matrix_exp = cv.intensity_to_binary(self.matrix, self.args.n_steps_pin)
        # loop over repetitions
        for i_r in np.arange(0, self.n_reps_layer):
            # loop over elements of expanded matrix
            for i_v in np.arange(0, matrix_exp.shape[3]):
                vol = matrix_exp[:, :, :, i_v]
                # loop over layers
                for i_z in np.arange(0, self.i_grid):
                    # select active columns
                    pins = self.col_pins[np.where(vol[:, :, i_z] != 0)].tolist()
                    GPIO.output(pins, True)
                    GPIO.output(self.ly_pins[i_z], True)
                    sleep(self.args.pin_delay)
                    GPIO.output(pins, False)
                    GPIO.output(self.ly_pins[i_z], False)


if __name__ == "__main__":
    print('Press CTRL+C to stop script')
    my_args, unknown = cv.my_parser().parse_known_args()
    if my_args.vis_type == 'cube':
        import RPi.GPIO as GPIO

    if my_args.vis_type == 'plot':
        cmd_str = f'python visualisation_demo.py --vis_type plot' + cv.args_to_cmd(my_args)
        os.system(cmd_str)

    elif my_args.vis_type == 'plot_binary':
        cmd_str = f'python visualisation_demo.py --vis_type plot_binary' + cv.args_to_cmd(my_args)
        os.system(cmd_str)

    elif my_args.vis_type == 'cube':
        visu = CubeSequence(my_args)
