from icecream import ic
from pathlib import Path

file_name = "r.in"
content = (Path(__file__).parent / file_name).read_text()
cal_list = content.split("\n\n")


sums = []
for e in cal_list:
    calories = e.strip().split("\n")
    sums.append(sum(map(int, calories)))
ic(sum(sorted(sums)[-3:]))

