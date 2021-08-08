from datetime import date
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


def prepare_plot(ax, x_axis, y_axis):

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


def run(frame_no):
    line.set_data(x_axis[:frame_no + 1], y_axis[:frame_no + 1])
    return line,


if __name__ == '__main__':

    day = date.today()

    fig, ax = plt.subplots(figsize=(5, 5))
    x_axis, y_axis = calculate_vertices(day)
    prepare_plot(ax, x_axis, y_axis)
    line, = ax.plot([], [], lw=1.5)
    ax.axis('off')

    ani = FuncAnimation(
        fig, run, frames=len(x_axis), interval=1, repeat=False, blit=True
    )
    plt.show()