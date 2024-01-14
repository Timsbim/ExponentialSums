from argparse import ArgumentParser
from itertools import islice, permutations
from multiprocessing import cpu_count, Pool
from pathlib import Path

from utils import animate, plot


# Parse command line
parser = ArgumentParser()
parser.add_argument('numbers', nargs='+', type=int)
group = parser.add_mutually_exclusive_group()
group.add_argument('-p', '--permutations', action='store_true')
group.add_argument('-a', '--animate', action='store_true')
parser.add_argument('-s', '--save-to', default=Path.cwd(), type=Path)
parser.add_argument('--size', default=5, type=int)
args = parser.parse_args()

# Check input for validity (all numbers positve)
for n in args.numbers:
    if n <= 0:
        parser.exit(1, 'Only positive numbers allowed!\n')

args.numbers = tuple(args.numbers)

# Plot
ns_str = ', '.join(map(str, args.numbers))
if args.permutations:
    
    print(f'Exponential sum plots for all permutations of {ns_str} ...')
    ns = tuple(sorted(args.numbers))
    save_to = args.save_to / '_'.join(map(str, ns))
    save_to.mkdir(parents=True, exist_ok=True)
    perms = permutations(ns)
    while True:
        nss = tuple(islice(perms, 6))
        if len(nss) == 0:
            break
        plot(nss, save_to)

else:
    
    args.save_to.mkdir(parents=True, exist_ok=True)
    if args.animate:
        print(f'Exponential sum animation for {ns_str} ...')
        animate(args.numbers, args.save_to, size=args.size)
    else:
        print(f'Exponential sum plot for {ns_str} ...')
        plot(args.numbers, args.save_to, size=args.size)

print('... finished.')
