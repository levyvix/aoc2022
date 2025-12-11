def solve(content):
    sacks = content.splitlines()

    total = 0
    for sack in sacks:
        midpoint = len(sack) // 2
        first = sack[:midpoint]
        second = sack[midpoint:]
        common = set(first).intersection(second)
        common = list(common)[0]
        if common == common.lower():
            total += ord(common) - 96
        elif common == common.upper():
            total += ord(common) - 38

    return total


def main():
    content = open(0).read()
    res = solve(content)
    print(res)


if __name__ == "__main__":
    main()
