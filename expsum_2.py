from pathlib import Path
from datetime import date, timedelta

import numpy as np
import matplotlib.pyplot as plt


WORKING_DIR = '/Users/me/etc'


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


if __name__ == '__main__':

    # Base directory
    base_path = Path(WORKING_DIR)
    base_path.mkdir(parents=True, exist_ok=True)

    # Setting start and end day
    start_day = date(2020, 1, 1)
    end_day = date(2020, 1, 31)

    # Creating plots for 6 days at a time
    one_day = timedelta(days=1)
    day = start_day
    while day <= end_day:

        file_name = str(day)
        fig = plt.figure(figsize=(10, 15))
        for i in range(1, min((end_day - day).days + 1, 6) + 1):

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
            sub = fig.add_subplot(3, 2, i)
            sub.set_xlim(x_0 - half_interval, x_0 + half_interval)
            sub.set_ylim(y_0 - half_interval, y_0 + half_interval)
            sub.axis('off')
            sub.plot(x_axis, y_axis, linewidth=1, color='darkblue')

            # Next day ...
            day = day + one_day

        # Saving plots in file
        file_name = f"{file_name} - {day}.png"
        file_path = base_path / file_name
        plt.savefig(file_path)
        plt.close('all')
