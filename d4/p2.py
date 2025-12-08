from icecream import ic
from pathlib import Path

file_name = "r.in"
content = (Path(__file__).parent / file_name).read_text()
ranges = content.splitlines()

pair = 0
for r in ranges:
    one, two = r.split(",")
    ones = list(map(int, one.split("-")))
    twos = list(map(int, two.split("-")))
    range_one = list(range(ones[0], ones[1] + 1))
    range_two = list(range(twos[0], twos[1] + 1))
    if len(set(range_one).intersection(set(range_two))) > 0:
        pair += 1
ic(pair)
