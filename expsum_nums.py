from argparse import ArgumentParser, RawDescriptionHelpFormatter
from itertools import islice, permutations
from pathlib import Path
from textwrap import dedent

from utils import animate, plot


# Parse command line
description = dedent('''\
    Generates plots of the lines between the partial sums of
    
        exp(2πi * (n / n_1 + ... + n**k / n_k))
    
    for n in 0, ..., lcm(n_1, ..., n_k).
    
    The plots can be static (.png) or animated (.gif). There's also an option
    to generate overviews for all the permutations of the given numbers.''')
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
    'numbers', nargs='+', type=int,
    help='numbers n_1, ..., n_k used for generating the sums'
)
group = parser.add_mutually_exclusive_group()
group.add_argument(
    '-p', '--permutations', action='store_true',
    help='''generate overview plots for all permutations of the given numbers
         (not allowed in comination with animation)'''
)
group.add_argument(
    '-a', '--animate', action='store_true',
    help='generate an animated .gif instead of a plain .png plot'
)
parser.add_argument(
    '-s', '--save-to', default=Path.cwd(), type=Path,
    help='folder for saving the files (default is cwd)'
)
parser.add_argument(
    '--size', default=5, type=int,
    help='''all plots are squares, the argument controls the side size 
         (default is 5)'''
)
args = parser.parse_args()

# Check input for validity (all numbers positve)
for n in args.numbers:
    if n <= 0:
        parser.exit(1, 'Only positive numbers allowed!\n')

args.numbers = tuple(args.numbers)

# Plot
ns_str = ', '.join(map(str, args.numbers))
ns = tuple(sorted(args.numbers))
save_to = args.save_to / '_'.join(map(str, ns))
save_to.mkdir(parents=True, exist_ok=True)
if args.permutations:
    
    print(f'Exponential sum plots for all permutations of {ns_str} ...')
    perms = permutations(ns)
    while True:
        nss = tuple(islice(perms, 6))
        if len(nss) == 0:
            break
        plot(nss, save_to)

else:
    
    if args.animate:
        print(f'Exponential sum animation for {ns_str} ...')
        animate(args.numbers, save_to, size=args.size)
    else:
        print(f'Exponential sum plot for {ns_str} ...')
        plot(args.numbers, save_to, size=args.size)

print('... finished.')
