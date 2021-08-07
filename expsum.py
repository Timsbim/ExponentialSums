from pathlib import Path
from datetime import date, timedelta

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


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

    @staticmethod
    def _calculate_vertices(day):

        year, month, day = day.year - 2000, day.month, day.day

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

    @staticmethod
    def _prepare_plot(ax, xaxis, yaxis):

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

    def plot(self, start=date.today(), end=date.today(), multi=False):
        if isinstance(start, str):
            start = date.fromisoformat(start)
        if isinstance(end, str):
            end = date.fromisoformat(end)
        if start == end:
            multi = False

        self._plot_path.mkdir(parents=True, exist_ok=True)

        one_day = timedelta(days=1)
        day = start
        if multi:
            # Creating plots for 6 days at a time
            while day <= end:
                start_day = day

                # Creating figure
                fig = plt.figure(figsize=(10, 15))
                for i in range(1, min((end - day).days + 1, 6) + 1):
                    # Creating ax
                    ax = fig.add_subplot(3, 2, i)
                    # Calculating vertices
                    xaxis, yaxis = self._calculate_vertices(day)
                    # Prepare plotting
                    self._prepare_plot(ax, xaxis, yaxis)
                    # Plotting
                    ax.axis('off')
                    ax.plot(xaxis, yaxis, linewidth=1.5)

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
                xaxis, yaxis = self._calculate_vertices(day)
                # Prepare plotting
                self._prepare_plot(ax, xaxis, yaxis)
                # Plotting
                ax.axis('off')
                ax.plot(xaxis, yaxis, linewidth=1.5)

                # Saving plot in file
                file_path = self._plot_path / f"{day}.png"
                plt.savefig(file_path)
                plt.close('all')

                # Next day ...
                day = day + one_day

    def animate(self, day=date.today()):
        if isinstance(day, str):
            day = date.fromisoformat(day)

        # Run-function to update the plot
        def run(frame_no):
            line.set_data(xaxis[:frame_no + 1], yaxis[:frame_no + 1])
            return line,

        fig, ax = plt.subplots(figsize=(5, 5))
        xaxis, yaxis = self._calculate_vertices(day)
        self._prepare_plot(ax, xaxis, yaxis)
        line, = ax.plot([], [], lw=1.5)
        ax.axis('off')

        ani = FuncAnimation(
            fig, run, frames=len(xaxis), interval=1, repeat=False, blit=True
        )
        plt.show()


e = ExpSum()
#e.plot()
#e.plot("2021-08-01", "2021-09-30")
e.plot("2021-10-01", "2021-12-31", multi=True)
#e.animate(date(2021, 9, 17))