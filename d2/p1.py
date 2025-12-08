from icecream import ic
from pathlib import Path

file_name = "r.in"
content = (Path(__file__).parent / file_name).read_text()
rounds = content.splitlines()

points = {"draw": 3, "lose": 0, "win": 6}
points_move = {"X": 1, "Y": 2, "Z": 3}
p = 0
for r in rounds:
    other, me = r.strip().split()
    if other == "A":
        if me == "X":
            result = "draw"
        elif me == "Y":
            result = "win"
        else:
            result = "lose"
    elif other == "B":
        if me == "X":
            result = "lose"
        elif me == "Y":
            result = "draw"
        else:
            result = "win"
    else:
        if me == "X":
            result = "win"
        elif me == "Y":
            result = "lose"
        else:
            result = "draw"
    p += points[result] + points_move[me]
ic(p)
