from pathlib import Path
from datetime import date, timedelta

import numpy as np
import matplotlib.pyplot as plt


class ExpSum:

    def __init__(self, plot_dir=None):
        if plot_dir is None:
            self._plot_path = Path.cwd()
        else:
            self._plot_path = Path(plot_dir)

    @property
    def plot_directory(self):
        return str(self._plot_path)

    @plot_directory.setter
    def plot_directory(self, plot_dir):
        self._plot_path = Path(plot_dir)

    @staticmethod
    def _calculate_vertices(day):

        year, month, day = day.year - 2000, day.month, day.day

        # Setting the length of the sum
        length = np.lcm.reduce((month, day, year)) + 1

        return np.add.accumulate(
            [
                np.exp(
                    2j * np.pi
                    * (pow(n, 1) / month + pow(n, 2) / day + pow(n, 3) / year)
                )
                for n in np.arange(length)
            ]
        )

    @staticmethod
    def _plot(ax, sums):
        # Axis-values: Re and Im of the sums
        xaxis = sums.real
        yaxis = sums.imag

        # Making sure the plot preserves the natural proportions
        xmin, xmax = np.min(xaxis), np.max(xaxis)
        ymin, ymax = np.min(yaxis), np.max(yaxis)

        # Calculating the centre point
        x0 = xmin + (xmax - xmin) / 2
        y0 = ymin + (ymax - ymin) / 2

        # Calculating the visible area around the centre point
        half_interval = max((xmax - xmin), (ymax - ymin)) / 2

        # Plotting
        ax.set_xlim(x0 - half_interval, x0 + half_interval)
        ax.set_ylim(y0 - half_interval, y0 + half_interval)
        ax.axis('off')
        ax.plot(xaxis, yaxis, linewidth=1.5)

    def plot(self, start=date.today(), end=date.today(), multi=False):
        if isinstance(start, str):
            start = date.fromisoformat(start)
        if isinstance(end, str):
            end = date.fromisoformat(end)
        if start == end:
            multi = False

        one_day = timedelta(days=1)
        day = start
        if multi:
            # Creating plots for 6 days at a time
            while day <= end:
                start_day = day

                # Creating figure
                fig = plt.figure(figsize=(10, 15))
                for i in range(1, min((end - day).days + 1, 6) + 1):
                    #Creating ax
                    ax = fig.add_subplot(3, 2, i)
                    # Calculating vertices
                    sums = self._calculate_vertices(day)
                    # Plotting
                    self._plot(ax, sums)

                # Next day ...
                day = day + one_day

                # Saving plots in file
                file_name = f"{start_day} - {day}.png"
                file_path = self._plot_path / file_name
                plt.savefig(file_path)
                plt.close('all')
        else:
            # Creating one plot for every day in the range between start and
            # end day
            day = start
            while day <= end:
                # Creating figure and ax
                fig, ax = plt.subplots(figsize=(5, 5))
                # Calculating vertices
                sums = self._calculate_vertices(day)
                # Plotting
                self._plot(ax, sums)
                # Saving plot in file
                file_path = self._plot_path / f"{day}.png"
                plt.savefig(file_path)
                plt.close('all')
                # Next day ...
                day = day + one_day

e = ExpSum()
print(e.plot_directory)
e.plot_directory = "C"
print(e.plot_directory)