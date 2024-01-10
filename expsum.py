from argparse import ArgumentParser
from cmath import exp
from datetime import date, datetime as dt, timedelta
from itertools import accumulate, groupby, islice
from math import lcm, pi as PI
from operator import attrgetter
from pathlib import Path

import matplotlib.pyplot as plt


def get_args():
    
    parser = ArgumentParser()
    parser.add_argument('-f', '--from', dest='start', default=date.today())
    parser.add_argument('-t', '--to', dest='end', default=date.today())
    parser.add_argument('-s', '--save-to', default=Path.cwd(), type=Path)
    parser.add_argument('-m', '--multi', action='store_true')
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
    
    return args.start, args.end, args.save_to, args.multi


def vertices(day):
    """See: https://www.johndcook.com/expsum/details.html"""    
    
    c, month, day, year = 2j * PI, day.month, day.day, day.year - 2_000
    sums = accumulate(
        exp(c * (n / month + n**2 / day + n**3 / year))
        for n in range(lcm(month, day, year) + 1)
    )

    return tuple(zip(*((s.real, s.imag) for s in sums)))


def plot_args(start, end, save_to, multi):
    
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
        
        # Package the days
        if multi:  # Six-packs if option multi selected
            while True:
                sixpack = tuple(islice(days, 0, 6))
                if len(sixpack) == 0:
                    break
                yield sixpack, ym_folder
        else:  # Single days
            yield from ((day, ym_folder) for day in days)


def prepare_plot(ax, x_axis, y_axis):
    
    # Making sure the plot preserves the natural proportions
    x_min, x_max = min(x_axis), max(x_axis)
    y_min, y_max = min(y_axis), max(y_axis)

    # Calculating the centre point
    x_0 = x_min + (x_max - x_min) / 2
    y_0 = y_min + (y_max - y_min) / 2

    # Calculating the visible area around the centre point
    half_interval = max((x_max - x_min), (y_max - y_min)) / 2

    # Adjust the axes accordingly
    ax.set_xlim(x_0 - half_interval, x_0 + half_interval)
    ax.set_ylim(y_0 - half_interval, y_0 + half_interval)


def plot(days, folder):

    if isinstance(days, tuple):  # Six-packs of days
        # Creating figure
        fig = plt.figure(figsize=(10, 15))
        for i, day in enumerate(days, start=1):
            # Creating ax
            ax = fig.add_subplot(3, 2, i)
            # Calculating vertices
            x_axis, y_axis = vertices(day)
            # Prepare plotting
            prepare_plot(ax, x_axis, y_axis)
            # Plotting
            ax.axis('off')
            ax.plot(x_axis, y_axis, linewidth=1.5)
    
        # Setting file path
        file_path = folder / f'{days[0]} - {days[-1]}.png'
    
    else:  # Single day
        day = days
        fig, ax = plt.subplots(figsize=(5, 5))
        # Calculating vertices
        x_axis, y_axis = vertices(day)
        # Prepare plotting
        prepare_plot(ax, x_axis, y_axis)
        # Plotting
        ax.axis('off')
        ax.plot(x_axis, y_axis, linewidth=1.5)
    
        # Setting file path
        file_path = folder / f'{day}.png'
    
    # Saving the plot
    plt.savefig(file_path)
    plt.close('all')
    print(f'{file_path.name} ready')


if __name__ == '__main__':

    start, end, save_to, multi = get_args()
    for days, path in plot_args(start, end, save_to, multi):
        plot(days, path)
