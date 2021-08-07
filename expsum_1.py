from pathlib import Path
from datetime import date, timedelta

import numpy as np
import matplotlib.pyplot as plt


WORKING_DIR = '/Users/me/etc'


def calculate_vertices(day):
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


if __name__ == '__main__':

    # Base directory
    base_path = Path(WORKING_DIR)
    base_path.mkdir(parents=True, exist_ok=True)

    # Setting start and end day
    start_day = date(2018, 9, 1)
    end_day = date(2020, 9, 1)

    # Creating one plot for every day in the range between start and end day
    one_day = timedelta(days=1)
    day = start_day
    while day <= end_day:

        # Setting output directories
        path = base_path / str(day.year) / str(day.month)
        path.mkdir(parents=True, exist_ok=True)

        # Calculating vertices
        x_axis, y_axis = calculate_vertices(day)

        # Making sure the plot preserves the natural proportions
        x_min, x_max = np.min(x_axis), np.max(x_axis)
        y_min, y_max = np.min(y_axis), np.max(y_axis)

        # Calculating the centre point
        x_0 = x_min + (x_max - x_min) / 2
        y_0 = y_min + (y_max - y_min) / 2

        # Calculating the visible area around the centre point
        half_interval = max((x_max - x_min), (y_max - y_min)) / 2

        # Plotting
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set_xlim(x_0 - half_interval, x_0 + half_interval)
        ax.set_ylim(y_0 - half_interval, y_0 + half_interval)
        ax.axis('off')
        ax.plot(x_axis, y_axis, linewidth=1.5)

        # Saving plot in file
        file_path = path / f"{day}.png"
        plt.savefig(file_path)
        plt.close('all')

        # Next day ...
        day = day + one_day
