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
        #self.master.attributes('-fullscreen', True)
        # init dummy visualization
        self.visu = cv.Visualization()
        # load default settings
        self.df = cv.defaults

        # Style
        style = ttk.Style()
        my_font = font.Font(family='Arial', size=50, weight='bold')
        my_font2 = font.Font(family='Arial', size=20, weight='bold')

        style.theme_use('alt')
        style.configure('bl.TButton', background='blue', foreground='white', borderwidth=4, focusthickness=3, font=my_font)
        style.configure('gr.TButton', background='green', foreground='white', borderwidth=4, focusthickness=3, font=my_font)
        style.configure('rd.TButton', background='red', foreground='white', borderwidth=4, focusthickness=3, font=my_font)
        style.map('gr.TButton', background=[('active', 'lightgreen'), ('pressed', 'red')])
        style.map('rd.TButton', background=[('active', 'lightred'), ('pressed', 'red')])

        # layout
        tk.Grid.rowconfigure(self.master, 0, weight=1)
        tk.Grid.rowconfigure(self.master, 1, weight=1)
        tk.Grid.columnconfigure(self.master, 0, weight=1)

        self.bts = tk.Frame(self.master)
        self.bts.grid(sticky='NSEW')

        tk.Grid.rowconfigure(self.bts, 0, weight=1)
        tk.Grid.rowconfigure(self.bts, 1, weight=1)
        tk.Grid.rowconfigure(self.bts, 2, weight=1)
        tk.Grid.columnconfigure(self.bts, 0, weight=1)
        tk.Grid.columnconfigure(self.bts, 1, weight=1)
        tk.Grid.columnconfigure(self.bts, 2, weight=1)

        # Buttons
        bts = {}
        for i_b in np.arange(0, len(self.df)):
            bt = ttk.Button(self.bts, text=self.df.loc[i_b].at['vis_name'], style='bl.TButton')
            bts[f'bt{i_b}'] = bt
            bt.bind('<Button-1>', self.click_bt)

        bts['bt_pause'] = ttk.Button(self.bts, text='start/stop', command=self.start_stop, style='rd.TButton')
        bts['bt_exit'] = ttk.Button(self.bts, text='exit', command=self.close_gui, style='rd.TButton')

        bts['bt0'].grid(row=0, column=0, sticky='NSEW')
        bts['bt1'].grid(row=0, column=1, sticky='NSEW')
        bts['bt2'].grid(row=0, column=2, sticky='NSEW')
        bts['bt3'].grid(row=1, column=0, sticky='NSEW')
        bts['bt4'].grid(row=1, column=1, sticky='NSEW')
        bts['bt5'].grid(row=1, column=2, sticky='NSEW')
        bts['bt_pause'].grid(row=2, column=1, sticky='NSEW')
        bts['bt_exit'].grid(row=2, column=2, sticky='NSEW')

        # time slider
        self.sl = tk.Frame(self.master)
        self.sl.grid(row=1, column=0, sticky='NSEW')
        tk.Grid.columnconfigure(self.sl, 0, weight=1)
        self.slid_val = tk.DoubleVar()
        self.slid_val.set(0.5)
        slid = tk.Scale(self.sl, font=my_font2, label='time between volumes (s):', tickinterval=0.25, resolution=0.01, from_=0.1, to=1, orient=tk.HORIZONTAL, variable=self.slid_val)
        slid.grid(row=0, column=0, sticky='NSEW')
        ttk.Button(self.bts, text='apply', command=self.set_time, style='gr.TButton').grid(row=2, column=0, sticky='NSEW')

    def set_time(self):
        time_step = self.slid_val.get()
        self.visu.update_time_step(time_step)

    def click_bt(self, event):
        my_args, unknown = cv.my_parser().parse_known_args()
        setattr(my_args, 'fname', event.widget['text'])
        time_step = self.df[self.df.vis_name == event.widget['text']].time_step.values[0]
        self.slid_val.set(time_step)
        setattr(my_args, 'time_step', time_step)

        #setattr(my_args, 'vis_type', 'cube')

        self.visu.close_animation()
        if my_args.vis_type == 'plot':
            self.visu = cv.PlotRun(args=my_args)
            self.visu.run_animation()
        elif my_args.vis_type == 'cube':
            self.visu = cv.CubeRun(args=my_args, root=self.master)
            self.visu.run_animation()

    def start_stop(self):
        self.visu.start_stop()

    def close_gui(self):
        self.visu.close_animation()
        sys.exit()


def main():
    root = tk.Tk()
    GuiRun(root)
    root.mainloop()


if __name__ == "__main__":
    main()

