import re
from icecream import ic
import sys

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def main():
    content = open(0).read()
    crates, moves = content.split("\n\n")
    crates = crates.splitlines()
    moves = moves.splitlines()
    digits = []
    for r, rows in enumerate(crates):
        for c, char in enumerate(rows):
            if char.isdigit():
                digits.append((r, c))

    crates_stacks = []
    for rd, cd in digits:
        stack = []
        i = 1
        while True:
            nr, nc = (rd - i, cd)
            if nr < 0:
                break
            cell = crates[nr][nc]
            if cell != " ":
                stack.append(cell)
                i += 1
            else:
                break
        crates_stacks.append(stack)

    digit_pattern = r"\d+"
    for move in moves:
        digits = re.findall(digit_pattern, move)
        nCrates = int(digits[0])
        crateFrom = int(digits[1])
        crateTo = int(digits[2])

        for _ in range(nCrates):
            d = (
                crates_stacks[crateFrom - 1].pop()
                if len(crates_stacks[crateFrom - 1]) > 0
                else None
            )
            if d:
                crates_stacks[crateTo - 1].append(d)
    ic("".join([c[-1] for c in crates_stacks]))


if __name__ == "__main__":
    main()
