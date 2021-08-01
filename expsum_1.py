from pathlib import Path
from datetime import date, timedelta

import numpy as np
import matplotlib.pyplot as plt


WORKING_DIR = '/Users/timus/Dropbox/Developing/Python/ExpSum/plots/days'


def calculate_vertices(year, month, day) -> np.array:

    # Normalizing year
    year -= 2000

    # Setting the length of the sum
    length = np.lcm.reduce((month, day, year)) + 1

    def vertices(n):
        return np.exp(
            2j * np.pi
               * (pow(n, 1) / month + pow(n, 2) / day + pow(n, 3) / year)
        )

    # Calculating vertices
    return np.add.accumulate([vertices(n) for n in np.arange(length)])


if __name__ == '__main__':

    # Base directory
    base_path = Path(WORKING_DIR)
    base_path.mkdir(parents=True, exist_ok=True)

    # Setting start and end day
    start_day = date(2018, 9, 1)
    end_day = date(2020, 9, 1)

    # Creating one plot for every day in the range between start and end day
    day = start_day
    while day <= end_day:

        # Setting output directories
        path = base_path / str(day.year) / str(day.month)
        path.mkdir(parents=True, exist_ok=True)

        # Calculating vertices
        sums = calculate_vertices(day.year, day.month, day.day)
        xaxis = sums.real
        yaxis = sums.imag

        # Making sure the plot preserves the natural proportions
        xmin, xmax = np.min(xaxis), np.max(xaxis)
        ymin, ymax = np.min(yaxis), np.max(yaxis)

        # Calculating the centre point
        x0 = xmin + (xmax-xmin) / 2
        y0 = ymin + (ymax-ymin) / 2

        # Calculating the visible area around the centre point
        half_interval = max((xmax-xmin), (ymax-ymin)) / 2

        # Plotting
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set_xlim(x0-half_interval, x0+half_interval)
        ax.set_ylim(y0-half_interval, y0+half_interval)
        ax.axis('off')
        ax.plot(xaxis, yaxis, linewidth=1.5)

        # Saving plot in file
        file_path = path / f"{day}.png"
        plt.savefig(file_path)
        plt.close('all')

        # Next day ...
        day = day + timedelta(days=1)
