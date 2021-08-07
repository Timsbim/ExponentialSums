from pathlib import Path
from datetime import date, timedelta

import numpy as np
import matplotlib.pyplot as plt


def calculate_vertices(year: int, month: int, day: int) -> np.array:
    """Function calculates the vertices of the plot(s):

     - The year is normalized (year = year - 2000)

     - Length of the plotted sum: LCM(month, day year) + 1
    """

    # Normalizing year
    year -= 2000

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
