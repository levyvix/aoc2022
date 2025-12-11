from icecream import ic
import sys
import json
from functools import cmp_to_key

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def compare(left, right):
    """
    Compare two packets.
    Returns: -1 if left < right (correct order)
             0 if left == right
             1 if left > right (wrong order)
    """
    # Both are integers
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return -1
        elif left > right:
            return 1
        else:
            return 0

    # Both are lists
    if isinstance(left, list) and isinstance(right, list):
        for l, r in zip(left, right):
            cmp = compare(l, r)
            if cmp != 0:
                return cmp
        # All equal so far, check lengths
        if len(left) < len(right):
            return -1
        elif len(left) > len(right):
            return 1
        else:
            return 0

    # Mixed types - convert int to list
    if isinstance(left, int):
        left = [left]
    else:
        right = [right]

    return compare(left, right)


def solve(input_data):
    """Parse input and solve the puzzle."""
    lines = input_data.strip().split('\n')

    packets = []
    for line in lines:
        if line:  # Skip blank lines
            packets.append(json.loads(line))

    # Add divider packets
    divider1 = [[2]]
    divider2 = [[6]]
    packets.append(divider1)
    packets.append(divider2)

    # Sort packets
    packets.sort(key=cmp_to_key(compare))

    # Find indices of divider packets (1-indexed)
    idx1 = packets.index(divider1) + 1
    idx2 = packets.index(divider2) + 1

    result = idx1 * idx2
    return result


def main():
    """Read from stdin and print result."""
    content = open(0).read().strip()
    result = solve(content)
    print(result)


if __name__ == "__main__":
    main()
