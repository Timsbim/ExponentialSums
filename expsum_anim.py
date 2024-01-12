from argparse import ArgumentParser
from cmath import exp
from datetime import date, datetime as dt, timedelta
from functools import partial
from itertools import accumulate, groupby
from math import lcm, pi as PI
from multiprocessing import cpu_count, Pool
from operator import attrgetter
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def get_args():

    parser = ArgumentParser()
    parser.add_argument('-f', '--from', dest='start', default=date.today())
    parser.add_argument('-t', '--to', dest='end', default=date.today())
    parser.add_argument('-s', '--save-to', default=Path.cwd(), type=Path)
    args = parser.parse_args()

    # Parse the dates (from, to) and check for viability
    err_msg = 'Error: wrong {}-date format: required is YYYY-MM-DD!\n'
    if isinstance(args.start, str):
        try:
            args.start = dt.strptime(args.start, '%Y-%m-%d').date()
        except ValueError:
            parser.exit(1, err_msg.format('from'))
    if isinstance(args.end, str):
        try:
            args.end = dt.strptime(args.end, '%Y-%m-%d').date()
        except ValueError:
            parser.exit(1, err_msg.format('to'))
    if args.end < args.start:
        parser.exit(1, 'Error: to-date has to be equal or after from-date!\n')

    return args.start, args.end, args.save_to


def vertices(day):
    """See: https://www.johndcook.com/expsum/details.html"""    

    c, month, day, year = 2j * PI, day.month, day.day, day.year - 2_000
    sums = accumulate(
        exp(c * (n / month + n**2 / day + n**3 / year))
        for n in range(lcm(month, day, year) + 1)
    )

    return tuple(zip(*((s.real, s.imag) for s in sums)))


def animate_args(start, end, save_to):

    # Create the days from start to end (inklusive)
    days = (
        start + timedelta(days=days)
        for days in range((end - start).days + 1)
    )

    # Group by year and month
    for (year, month), days in groupby(days, key=attrgetter('year', 'month')):
        # Create the save-folders
        ym_folder = save_to / f'{year}' / f'{month:0>2}'
        ym_folder.mkdir(parents=True, exist_ok=True)
        yield from ((day, ym_folder) for day in days)


def prepare_axes(ax, x_axis, y_axis):

    # Making sure the plot preserves the natural proportions
    x_min, x_max = min(x_axis), max(x_axis)
    y_min, y_max = min(y_axis), max(y_axis)

    # Calculating the centre point
    x_0 = x_min + (x_max - x_min) / 2
    y_0 = y_min + (y_max - y_min) / 2

    # Calculating the visible area around the centre point
    half_interval = max((x_max - x_min), (y_max - y_min)) / 2

    # Size the axis and make them invisible
    ax.set_xlim(x_0 - half_interval, x_0 + half_interval)
    ax.set_ylim(y_0 - half_interval, y_0 + half_interval)
    ax.axis('off')


def update_frames(no, *, line, x, y):
    line.set_data(x[:no], y[:no])
    return (line,)


def animate(day, folder, *, max_size=500, duration=5_000):

    # Setup figure and axes
    x_axis, y_axis = vertices(day)
    fig, ax = plt.subplots(figsize=(5, 5))
    prepare_axes(ax, x_axis, y_axis)
    line, = ax.plot([], [], lw=1.5)

    # If number of points is too high: increase step size (number of segments
    # added in one animation step)
    size = len(x_axis)
    chunksize = max(1, size // max_size)
    if (rest := size % chunksize) != 0:
        size += chunksize - rest
    frames = range(1, size + 1, chunksize)

    # Make sure that the duration of the animation is approximately duration
    # many milliseconds
    interval = max(1, duration // (size // chunksize))

    # Create and save animation
    file_path = folder / f'{day}.gif'
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
    print(f'   {file_path} ... ready.', flush=True)


if __name__ == '__main__':

    start, end, save_to = get_args()
    print(f'Creating exponential sum animations from {start} to {end} ...')
    args = animate_args(start, end, save_to)
    if (end - start).days > 4 and cpu_count() >= 4:
        with Pool(cpu_count() // 2) as pool:
            pool.starmap(animate, args)
    else:
        for day, folder in args:
            animate(day, folder)
    print('... finished.')
