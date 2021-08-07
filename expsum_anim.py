from datetime import date
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


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


def prepare_plot(ax, xaxis, yaxis):

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


def run(frame_no):
    line.set_data(xaxis[:frame_no + 1], yaxis[:frame_no + 1])
    return line,


if __name__ == '__main__':

    day = date.today()

    fig, ax = plt.subplots(figsize=(5, 5))
    xaxis, yaxis = calculate_vertices(day)
    prepare_plot(ax, xaxis, yaxis)
    line, = ax.plot([], [], lw=1.5)
    ax.axis('off')

    ani = FuncAnimation(
        fig, run, frames=len(xaxis), interval=1, repeat=False, blit=True
    )
    plt.show()