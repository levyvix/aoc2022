import sys

from icecream import ic

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def solve(content: str) -> int:
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
    return p


def main():
    content = open(0).read()
    p = solve(content)

    print(p)


if __name__ == "__main__":
    main()
