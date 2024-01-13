from argparse import ArgumentParser
from datetime import date, datetime as dt, timedelta
from itertools import groupby, islice
from multiprocessing import cpu_count, Pool
from operator import itemgetter
from pathlib import Path

from utils import animate, plot


def arguments():
    
    parser = ArgumentParser()
    parser.add_argument('-f', '--from', dest='start', default=date.today())
    parser.add_argument('-t', '--to', dest='end', default=date.today())
    parser.add_argument('-s', '--save-to', default=Path.cwd(), type=Path)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-m', '--multi', action='store_true')
    group.add_argument('-a', '--animate', action='store_true')
    args = parser.parse_args()

    # Parse the dates (from, to) and check for viability
    err_msg = 'Error: wrong {}-date format: required is YYYY-MM-DD!\n'
    if isinstance(args.start, str):
        try:
            args.start = dt.strptime(args.start, '%Y-%m-%d').date()
        except ValueError:
            parser.exit(1, err_msg.format('from'))
    if isinstance(args.end, str):
        try:
            args.end = dt.strptime(args.end, '%Y-%m-%d').date()
        except ValueError:
            parser.exit(1, err_msg.format('to'))
    if args.end < args.start:
        parser.exit(1, 'Error: to-date has to be equal or after from-date!\n')
    
    return args


def days(start, end):
    for days in range((end - start).days + 1):
        day = start + timedelta(days=days)
        yield day.month, day.day, day.year % 100


def plot_arguments(start, end, save_to, multi):
    
    # Group by year and month
    nss = days(start, end)
    for (year, month), nss in groupby(nss, key=itemgetter(2, 0)):
        # Create the save-folders
        ym_folder = save_to / f'{year}' / f'{month:0>2}'
        ym_folder.mkdir(parents=True, exist_ok=True)
        
        # Package the days
        if multi:  # Six-packs if option multi selected
            while True:
                sixpack = tuple(islice(nss, 0, 6))
                if len(sixpack) == 0:
                    break
                yield sixpack, ym_folder
        else:  # Single days
            yield from ((ns, ym_folder) for ns in nss)


if __name__ == '__main__':

    args = arguments()
    start, end = args.start, args.end
    if args.animate:
        
        print(f'Exponential sum animations from {start} to {end} ...')
        args = plot_arguments(args.start, args.end, args.save_to)
        if (end - start).days > 4 and cpu_count() >= 4:
            with Pool(cpu_count() // 2) as pool:
                pool.starmap(animate, args)
        else:
            for day, folder in args:
                animate(day, folder)
    
    else:
        
        print(f'Exponential sum plots from {start} to {end} ...')
        args = plot_argumentss(start, end, args.save_to, args.multi)
        if (end - start).days >= 12 and cpu_count() >= 4:
            with Pool(cpu_count() // 2) as pool:
                pool.starmap(plot, args)
        else:
            for days, folder in args:
                plot(days, folder)
    
    print('... finished.')
