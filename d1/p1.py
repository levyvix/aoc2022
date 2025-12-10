from icecream import ic
import sys

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def main():
    content = open(0).read()
    cal_list = content.split("\n\n")

    sums = []
    for e in cal_list:
        calories = e.strip().split("\n")
        sums.append(sum(map(int, calories)))
    ic(max(sums))


if __name__ == "__main__":
    main()

