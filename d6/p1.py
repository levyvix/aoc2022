from icecream import ic
import sys

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def main():
    content = open(0).read().strip()

    l, r = 0, 3
    while r <= len(content):
        targets = content[l : r + 1]
        if len(targets) != len(set(targets)):
            l += 1
            r += 1
        else:
            break
    ic(r + 1)


if __name__ == "__main__":
    main()
