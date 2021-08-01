import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


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


def data_gen(year, month, day):
    for s in calculate_vertices(year, month, day):
        yield s.real, s.imag


def init_gen(year, month, day):
    def init():
        # Getting values to adjust the ax
        sums = calculate_vertices(year, month, day)
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

        # Plotting and saving in file
        ax.set_xlim(x0-half_interval, x0+half_interval)
        ax.set_ylim(y0-half_interval, y0+half_interval)

        return line,

    return init


def run(data):
    # Updating the data
    x, y = data
    xdata.append(x)
    ydata.append(y)
    line.set_data(xdata, ydata)

    return line,


if __name__ == '__main__':

    fig, ax = plt.subplots(figsize=(5, 5))
    line, = ax.plot([], [], lw=1.5)
    ax.axis('off')
    xdata, ydata = [], []

    date = (2021, 9, 17)
    ani = FuncAnimation(
        fig,
        run,
        data_gen(*date),
        interval=1,
        init_func=init_gen(*date),
        repeat=False,
        blit=True
    )
    plt.show()
