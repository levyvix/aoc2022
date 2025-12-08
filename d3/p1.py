from icecream import ic
from pathlib import Path

file_name = "r.in"
content = (Path(__file__).parent / file_name).read_text()
sacks = content.splitlines()


in_common = []
total = 0
for sack in sacks:
    midpoint = len(sack) // 2
    first = sack[:midpoint]
    second = sack[midpoint:]
    common = set(first).intersection(second)
    common = list(common)[0]
    if common == common.lower():
        total += ord(common) - 96
    elif common == common.upper():
        total += ord(common) - 38

ic(total)
