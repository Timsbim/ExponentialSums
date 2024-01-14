from cmath import exp
from functools import partial
from itertools import accumulate
from math import lcm, pi as PI, prod

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def vertices(ns):
    """See: https://www.johndcook.com/expsum/details.html"""
    c = 2j * PI
    cs = tuple(c / n for n in ns)
    zs = accumulate(
        prod(exp(c * n**e) for e, c in enumerate(cs, start=1))
        for n in range(lcm(*ns) + 1)
    )

    return tuple(zip(*((z.real, z.imag) for z in zs)))


def prepare_axes(ax, x_axis, y_axis):
    
    # Making sure the plot preserves the natural proportions
    x_min, x_max = min(x_axis), max(x_axis)
    y_min, y_max = min(y_axis), max(y_axis)

    # Calculating the centre point
    x_0 = x_min + (x_max - x_min) / 2
    y_0 = y_min + (y_max - y_min) / 2

    # Calculating the visible area around the centre point
    half_interval = max((x_max - x_min), (y_max - y_min)) / 2 + 0.5

    # Adjust the axes accordingly
    ax.set_xlim(x_0 - half_interval, x_0 + half_interval)
    ax.set_ylim(y_0 - half_interval, y_0 + half_interval)
    ax.axis('off')


def plot(nss, folder, size=5):

    if isinstance(nss[0], tuple):
        
        # Creating figure
        fig = plt.figure(figsize=(10, 15))
        for i, ns in enumerate(nss, start=1):
            # Creating ax
            ax = fig.add_subplot(3, 2, i, title='-'.join(map(str, ns)))
            # Calculating vertices
            x_axis, y_axis = vertices(ns)
            # Prepare plotting
            prepare_axes(ax, x_axis, y_axis)
            # Plotting
            ax.axis('off')
            ax.plot(x_axis, y_axis, linewidth=1.5)

        # Setting file path
        numbers_from = '-'.join(map(str, nss[0]))
        numbers_to = '-'.join(map(str, nss[-1]))
        file_path = folder / f'{numbers_from}_{numbers_to}.png'
    
    else:
    
        ns = nss
        fig, ax = plt.subplots(figsize=(size, size))
        # Calculating vertices
        x_axis, y_axis = vertices(ns)
        # Prepare plotting
        prepare_axes(ax, x_axis, y_axis)
        # Plotting
        ax.axis('off')
        ax.plot(x_axis, y_axis, linewidth=1.5)
    
        # Setting file path
        numbers = '-'.join(map(str, ns))
        file_path = folder / f'{numbers}.png'
    
    # Saving the plot
    plt.savefig(file_path)
    plt.close('all')
    print(f'\t{file_path} ... ready.', flush=True)


def update_frames(no, *, line, x, y):
    line.set_data(x[:no], y[:no])
    return (line,)


def animate(ns, folder, size=5, *, max_len=500, duration=5_000):

    # Setup figure and axes
    x_axis, y_axis = vertices(ns)
    fig, ax = plt.subplots(figsize=(size, size))
    prepare_axes(ax, x_axis, y_axis)
    line, = ax.plot([], [], lw=1.5)
    
    # If number of points is too high: increase step size (number of
    # segments added in one animation step)
    length = len(x_axis)
    chunksize = max(1, length // max_len)
    if (rest := length % chunksize) != 0:
        length += chunksize - rest
    frames = range(1, length + 1, chunksize)
    
    # Make sure that the duration of the animation is approximately
    # duration many milliseconds
    interval = max(1, duration // (length // chunksize))
    
    # Create and save animation
    numbers = '-'.join(map(str, ns))
    file_path = folder / f'{numbers}.gif'
    FuncAnimation(
        fig=fig,
        func=partial(update_frames, line=line, x=x_axis, y=y_axis),
        frames=frames,
        interval=interval,
        repeat=True,
        repeat_delay=1_000,
        blit=True
    ).save(file_path, writer='pillow')
    plt.close()
    print(f'\t{file_path} ... ready.', flush=True)
