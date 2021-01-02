import cubeventure as cv

#scp ~/code/cubeventure/sequences/sphere.npy pi@192.168.178.71:/home/pi/myCode/cubeventure/sequences/sphere.npy

if __name__ == "__main__":
    my_args, unknown = cv.my_parser().parse_known_args()
    setattr(my_args, 'vis_type', 'cube')

    print(my_args)

    if my_args.vis_type == 'plot':
        visu = cv.PlotRun(my_args)
        visu.run_animation()

    elif my_args.vis_type == 'plot_binary':
        visu = cv.PlotRun(my_args)
        visu.run_animation()

    elif my_args.vis_type == 'cube':
        visu = cv.CubeRun(my_args)