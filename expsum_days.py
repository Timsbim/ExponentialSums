from argparse import ArgumentParser, RawDescriptionHelpFormatter
from datetime import date, datetime as dt, timedelta
from itertools import groupby, islice
from multiprocessing import cpu_count, Pool
from operator import itemgetter
from pathlib import Path
from textwrap import dedent

from utils import animate, plot


def arguments():

    description = dedent('''\
        Generates plots of the lines between the partial sums of

            exp(2πi * (n / month + n**2 / day + n**3 / year))

        for n in 0, ..., lcm(month, day, year). For year only the last two digits
        are used (year mod 100).

        The plots can be static (.png) or animated (.gif). There's also an option
        to generate overviews for the given day range in form of six days per
        plot.''')
    epilog = dedent('''\
        The idea to look at these fascinating images comes from John D. Cook's
        exponential sum of the day (https://www.johndcook.com/expsum/). Please
        visit his website!''')
    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description=description,
        epilog=epilog
    )
    parser.add_argument(
        '-f', '--from', dest='start', default=date.today(),
        help='first day (YYYY-MM-DD) of the day range (default is today)'
    )
    parser.add_argument(
        '-t', '--to', dest='end', default=date.today(),
        help='last day (YYYY-MM-DD) of the day range (default is today)'
    )
    parser.add_argument(
        '-s', '--save-to', default=Path.cwd(), type=Path,
        help='folder for saving the files (default is cwd)'
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-m', '--multi', action='store_true',
        help='''generate overview plots for the given day range (not allowed 
             in comination with animation)'''
    )
    group.add_argument(
        '-a', '--animate', action='store_true',
        help='generate an animated .gif instead of a plain .png plot'
    )
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
    if (
        args.start.year % 100 == 0
          or args.end.year % 100 == 0
          or args.start.year // 100 < args.end.year // 100
    ):
        parser.exit(1, "Error: day range can't contain turn of century years\n")
    
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
    pargs = plot_arguments(start, end, args.save_to, args.multi)
    if args.animate:
        
        print(f'Exponential sum animations from {start} to {end} ...')
        if (end - start).days > 4 and cpu_count() >= 4:
            with Pool(cpu_count() // 2) as pool:
                pool.starmap(animate, pargs)
        else:
            for day, folder in pargs:
                animate(day, folder)
    
    else:
        
        print(f'Exponential sum plots from {start} to {end} ...')
        if (end - start).days >= 12 and cpu_count() >= 4:
            with Pool(cpu_count() // 2) as pool:
                pool.starmap(plot, pargs)
        else:
            for days, folder in pargs:
                plot(days, folder)
    
    print('... finished.')
