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
    if ones[0] <= twos[0] and ones[1] >= twos[1]:
        pair += 1
    elif twos[0] <= ones[0] and twos[1] >= ones[1]:
        pair += 1
ic(pair)
