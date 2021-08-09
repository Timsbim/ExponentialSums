from pathlib import Path
from datetime import date, timedelta
from itertools import islice
from multiprocessing import Pool

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def _calculate_vertices(dt_day):
    year, month, day = dt_day.year - 2000, dt_day.month, dt_day.day

    # Setting the length of the sum
    length = np.lcm.reduce((month, day, year)) + 1

    sums = np.add.accumulate(
        [
            np.exp(
                2j * np.pi
                * (pow(n, 1) / month + pow(n, 2) / day + pow(n, 3) / year)
            )
            for n in np.arange(length)
        ]
    )

    return sums.real, sums.imag


def _prepare_plot(ax, x_axis, y_axis):
    # Making sure the plot preserves the natural proportions
    x_min, x_max = np.min(x_axis), np.max(x_axis)
    y_min, y_max = np.min(y_axis), np.max(y_axis)

    # Calculating the centre point
    x_0 = x_min + (x_max - x_min) / 2
    y_0 = y_min + (y_max - y_min) / 2

    # Calculating the visible area around the centre point
    half_interval = max((x_max - x_min), (y_max - y_min)) / 2

    # Plotting
    ax.set_xlim(x_0 - half_interval, x_0 + half_interval)
    ax.set_ylim(y_0 - half_interval, y_0 + half_interval)


def _plot_args(start, end, multi):
    days = (
        start + timedelta(days=days) for days in range((end - start).days + 1)
    )
    if multi:
        while True:
            s = tuple(islice(days, 0, 6))
            if len(s) > 0:
                yield s
            else:
                break
    else:
        yield from days


def _plot(days, path):

    if isinstance(days, tuple):  # 6-packs :) of days
        # Creating figure
        fig = plt.figure(figsize=(10, 15))
        for i, day in enumerate(days, start=1):
            # Creating ax
            ax = fig.add_subplot(3, 2, i)
            # Calculating vertices
            x_axis, y_axis = _calculate_vertices(day)
            # Prepare plotting
            _prepare_plot(ax, x_axis, y_axis)
            # Plotting
            ax.axis('off')
            ax.plot(x_axis, y_axis, linewidth=1.5)

        # Saving plots in file
        file_path = path / f"{days[0]} - {days[-1]}.png"
        plt.savefig(file_path)
        plt.close('all')
    else:  # Single days
        day = days
        fig, ax = plt.subplots(figsize=(5, 5))
        # Calculating vertices
        x_axis, y_axis = _calculate_vertices(day)
        # Prepare plotting
        _prepare_plot(ax, x_axis, y_axis)
        # Plotting
        ax.axis('off')
        ax.plot(x_axis, y_axis, linewidth=1.5)

        # Saving plot in file
        file_path = path / f"{day}.png"
        plt.savefig(file_path)
        plt.close('all')


class ExpSum:

    def __init__(self, plot_dir=None):
        if plot_dir is None:
            self._plot_path = Path.cwd() / "plots"
        else:
            self._plot_path = Path(plot_dir)

    @property
    def plot_directory(self):
        return str(self._plot_path)

    @plot_directory.setter
    def plot_directory(self, plot_dir):
        self._plot_path = Path(plot_dir)

    def plot(self, start=date.today(), end=date.today(), multi=False):
        if isinstance(start, str):
            start = date.fromisoformat(start)
        if isinstance(end, str):
            end = date.fromisoformat(end)
        if start == end:
            multi = False

        # Creating plot folder
        self._plot_path.mkdir(parents=True, exist_ok=True)

        # Preparing the arguments for the Pool: args and number of arguments
        args = (
            (days, self._plot_path) for days in _plot_args(start, end, multi)
        )
        num_args = (end - start).days + 1
        if multi:
            num_args, r = divmod(num_args, 6)
            if r:
                num_args += 1

        with Pool(min(num_args, 12)) as p:
            p.starmap(_plot, args)

    def animate(self, day=date.today(), save=False):
        if isinstance(day, str):
            day = date.fromisoformat(day)

        # Run-function to update the plot
        def run(frame_no):
            line.set_data(x_axis[:frame_no + 1], y_axis[:frame_no + 1])
            return line,

        fig, ax = plt.subplots(figsize=(5, 5))
        x_axis, y_axis = _calculate_vertices(day)
        _prepare_plot(ax, x_axis, y_axis)
        line, = ax.plot([], [], lw=1.5)
        ax.axis('off')

        ani = FuncAnimation(
            fig, run, frames=len(x_axis), interval=1, repeat=False, blit=True
        )
        if save:
            file_path = self._plot_path / f"{day}.gif"
            ani.save(file_path)
        plt.show()


if __name__ == "__main__":  # Multiprocessing -- shielding the process creation

    es = ExpSum()
    es.plot()
    es.plot("2021-08-01", "2021-08-30")
    es.plot("2021-10-01", "2021-12-31", multi=True)
    es.animate(save=True)

