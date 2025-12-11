from icecream import ic
import sys

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def solve(content):
    rounds = content.splitlines()

    points = {"draw": 3, "lose": 0, "win": 6}
    # X lose
    # Y draw
    # Z win
    p = 0
    for r in rounds:
        other, me = r.strip().split()
        if other == "A":  # he choose rock
            if me == "X":  # i need to lose, so choose scisor
                result = "lose"
                p += 3
            elif me == "Y":
                result = "draw"
                p += 1
            else:
                result = "win"
                p += 2
        elif other == "B":
            if me == "X":
                result = "lose"
                p += 1
            elif me == "Y":
                result = "draw"
                p += 2
            else:
                result = "win"
                p += 3
        else:
            if me == "X":
                result = "lose"
                p += 2
            elif me == "Y":
                result = "draw"
                p += 3
            else:
                result = "win"
                p += 1
        p += points[result]
    return p


def main():
    content = open(0).read()
    res = solve(content)
    print(res)


if __name__ == "__main__":
    main()
