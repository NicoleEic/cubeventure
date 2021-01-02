import tkinter as tk
from tkinter import ttk
from tkinter import font

import numpy as np
import cubeventure as cv
import sys


class GuiRun:
    def __init__(self, master):
        self.master = master
        self.master.title("Cubeventure")
        self.master.attributes('-fullscreen', True)

        self.visu = cv.Visualization()

        self.mapping = {'1': 'sequence',
                        '2': 'rain',
                        '3': 'sphere',
                        '4': 'fillup',
                        '5': 'intensity',
                        '6': 'wave'}

        tk.Grid.rowconfigure(self.master, 0, weight=1)
        tk.Grid.columnconfigure(self.master, 0, weight=1)

        self.bts = tk.Frame(self.master)
        self.bts.grid(sticky='NSEW')

        tk.Grid.rowconfigure(self.bts, 0, weight=1)
        tk.Grid.rowconfigure(self.bts, 1, weight=1)
        tk.Grid.rowconfigure(self.bts, 2, weight=1)
        tk.Grid.columnconfigure(self.bts, 0, weight=1)
        tk.Grid.columnconfigure(self.bts, 1, weight=1)
        tk.Grid.columnconfigure(self.bts, 2, weight=1)

        style = ttk.Style()
        my_font = font.Font(family='Arial', size=50, weight='bold')
        style.theme_use('alt')
        style.configure('TButton', background='blue', foreground='white', borderwidth=4, focusthickness=3, font=my_font)
        style.map('TButton', background=[('active', 'lightblue'), ('pressed', 'red')])

        n_bts = 6
        bts = {}
        for i_b in np.arange(1, n_bts+1):
            bt = ttk.Button(self.bts, text=self.mapping[f'{i_b}'])
            bts[f'bt{i_b}'] = bt
            bt.bind('<Button-1>', self.click_bt)

        bts['bt7'] = ttk.Button(self.bts, text='start/stop', command=self.start_stop)
        bts['bt8'] = ttk.Button(self.bts, text='exit', command=self.close)

        bts['bt1'].grid(row=0, column=0, sticky='NSEW')
        bts['bt2'].grid(row=0, column=1, sticky='NSEW')
        bts['bt3'].grid(row=0, column=2, sticky='NSEW')
        bts['bt4'].grid(row=1, column=0, sticky='NSEW')
        bts['bt5'].grid(row=1, column=1, sticky='NSEW')
        bts['bt6'].grid(row=1, column=2, sticky='NSEW')
        bts['bt7'].grid(row=2, column=0, sticky='NSEW')
        bts['bt8'].grid(row=2, column=2, sticky='NSEW')


    def click_bt(self, event):
        visu_name = event.widget['text']
        my_args, unknown = cv.my_parser().parse_known_args()
        setattr(my_args, 'fname', visu_name)
        #setattr(my_args, 'vis_type', 'cube')

        if my_args.vis_type == 'plot':
            self.visu = cv.PlotRun(args=my_args)
            self.visu.run_animation()
        elif my_args.vis_type == 'cube':
            self.visu = cv.CubeRun(args=my_args, root=self.master)
            self.visu.run_animation()

    def start_stop(self):
        self.visu.ani_running = False
        self.visu.start_stop()
        
    def close(self):
        sys.exit()


def main():
    root = tk.Tk()
    GuiRun(root)
    root.mainloop()


if __name__ == "__main__":
    main()

