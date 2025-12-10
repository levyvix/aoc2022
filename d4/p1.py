from icecream import ic
import sys

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def main():
    content = open(0).read()
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


if __name__ == "__main__":
    main()
