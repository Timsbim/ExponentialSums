from cmath import exp, isclose
from datetime import date, timedelta
from itertools import accumulate, combinations
from math import lcm, pi as PI
from timeit import timeit


def vertices_1(day):
    """See: https://www.johndcook.com/expsum/details.html"""       
    c, month, day, year = 2j * PI, day.month, day.day, day.year % 100
    sums = accumulate(
        exp(c * (n / month + n**2 / day + n**3 / year))
        for n in range(lcm(month, day, year) + 1)
    )

    return tuple(zip(*((s.real, s.imag) for s in sums)))


def vertices_2(day):
    """See: https://www.johndcook.com/expsum/details.html"""
    month, day, year = day.month, day.day, day.year % 100
    m = lcm(month, day, year)
    c, cm, cd, cy = 2j * PI / m, m // month, m // day, m // year
    sums = accumulate(
        exp(c * (cm * n + cd * n**2 + cy * n**3)) for n in range(m + 1)
    )

    return tuple(zip(*((s.real, s.imag) for s in sums)))


def vertices_3(day):
    """See: https://www.johndcook.com/expsum/details.html"""
    c, month, day, year = 2j * PI, day.month, day.day, day.year % 100
    cm, cd, cy = c / month, c / day, c / year
    sums = accumulate(
        exp(cm * n + cd * n**2 + cy * n**3)
        for n in range(lcm(month, day, year) + 1)
    )

    return tuple(zip(*((s.real, s.imag) for s in sums)))


def vertices_4(day):
    """See: https://www.johndcook.com/expsum/details.html"""
    c, month, day, year = 2j * PI, day.month, day.day, day.year % 100
    cm, cd, cy = c / month, c / day, c / year
    sums = accumulate(
        exp(cm * n) * exp(cd * n**2) * exp(cy * n**3)
        for n in range(lcm(month, day, year) + 1)
    )

    return tuple(zip(*((s.real, s.imag) for s in sums)))


def timing(funcs):

    def test(func, days):
        for day in days:
            func(day)
    
    start = date(2022, 1, 1)
    days = tuple(start + timedelta(days=days) for days in range(365 * 3))
    msg = 'Duration version {}: {:.2f} seconds'
    for n in range(1, 5):
        t = timeit(f'test(funcs[{n}], days)', globals=locals(), number=10)
        print(msg.format(n, t))


#funcs = {1: vertices_1, 2: vertices_2, 3: vertices_3, 4: vertices_4}
#timing(funcs)


def diffs(funcs):
    start = date(2022, 1, 1)
    for n1, n2 in combinations(range(1, 5), r=2):
        maximum, max_day = float('-inf'), start
        for day in (start + timedelta(days=days) for days in range(365)):
            xs1, ys1 = funcs[n1](day)
            xs2, ys2 = funcs[n2](day)
            err = sum(
                abs(x1 - x2) + abs(y1 - y2)
                for x1, x2, y1, y2 in zip(xs1, xs2, ys1, ys2)
            ) / len(xs1)
            if maximum < err:
                maximum = err
                max_day = day
        
        print(max_day, maximum)


#diffs(funcs)


eps = 1e-2
start = date(2024, 1, 1)
for day in (start + timedelta(days=days) for days in range(365)):
    xs, ys = vertices_4(day)
    if not isclose(xs[0] + 1j * ys[0], xs[-1] + 1j * ys[-1], abs_tol=eps):
        m = lcm(day.month, day.day, day.year % 100)
        print(f'{day}: {m}')
        #print(abs(xs[0] - xs[-1]), abs(ys[0] - ys[-1]))
