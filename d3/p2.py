from icecream import ic
import sys
from itertools import batched


ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def prio(common):
    if common == common.lower():
        return ord(common) - 96
    else:
        return ord(common) - 38


def main():
    content = open(0).read()
    sacks = content.splitlines()
    groups = batched(sacks, n=3)

    total = 0
    for f, s, t in groups:
        common = set(f).intersection(s).intersection(t)
        common = list(common)[0]
        total += prio(common)

    ic(total)


if __name__ == "__main__":
    main()
