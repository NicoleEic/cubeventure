import tkinter as tk
import numpy as np
import pandas as pd
import cubeventure as cv


class GuiRun:
    def __init__(self, master):
        self.master = master
        self.master.title("Cubeventure")
        self.master.attributes('-fullscreen', True)

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
        tk.Grid.columnconfigure(self.bts, 0, weight=1)
        tk.Grid.columnconfigure(self.bts, 1, weight=1)
        tk.Grid.columnconfigure(self.bts, 2, weight=1)

        n_bts = 6
        bts = {}
        for i_b in np.arange(1, n_bts+1):
            bt = tk.Button(self.bts, text=self.mapping[f'{i_b}'])
            bts[f'bt{i_b}'] = bt
            bt.bind('<Button-1>', self.click_bt)

        bts['bt1'].grid(row=0, column=0, sticky='NSEW')
        bts['bt2'].grid(row=0, column=1, sticky='NSEW')
        bts['bt3'].grid(row=0, column=2, sticky='NSEW')
        bts['bt4'].grid(row=1, column=0, sticky='NSEW')
        bts['bt5'].grid(row=1, column=1, sticky='NSEW')
        bts['bt6'].grid(row=1, column=2, sticky='NSEW')

    def click_bt(self, event):
        visu_name = event.widget['text']
        my_args, unknown = cv.my_parser().parse_known_args()
        setattr(my_args, 'sequence', visu_name)
        cv.PlotRun(my_args)


def main():
    root = tk.Tk()
    GuiRun(root)
    root.mainloop()


if __name__ == "__main__":
    main()

