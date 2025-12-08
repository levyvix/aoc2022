from icecream import ic
from pathlib import Path

file_name = "r.in"
content = (Path(__file__).parent / file_name).read_text().strip()

l, r = 0, 13
while r <= len(content):
    targets = content[l : r + 1]
    if len(targets) != len(set(targets)):
        l += 1
        r += 1
    else:
        break
ic(r + 1)
