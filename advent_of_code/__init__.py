import argparse

def solve():
    parser = argparse.ArgumentParser()
    parser.add_argument('year', type=int, help='year')
    parser.add_argument('day', type=int, help='day')
    parser.add_argument('part', type=str, help='part')

    args = parser.parse_args()
    print(args.year, args.day, args.part)

