from icecream import ic
from pathlib import Path
from itertools import batched


def prio(common):
    if common == common.lower():
        return ord(common) - 96
    else:
        return ord(common) - 38


file_name = "r.in"
content = (Path(__file__).parent / file_name).read_text()
sacks = content.splitlines()
groups = batched(sacks, n=3)


in_common = []
total = 0
for f, s, t in groups:
    common = set(f).intersection(s).intersection(t)
    common = list(common)[0]
    total += prio(common)


ic(total)
