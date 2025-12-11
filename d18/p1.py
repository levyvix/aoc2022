from icecream import ic
import sys
from collections import deque

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def solve(input_data):
    """Count exposed faces of lava droplet cubes."""
    lines = input_data.strip().split('\n')

    # Parse all cube coordinates
    cubes = set()
    for line in lines:
        line = line.strip()
        if not line or '-' in line or 'Example' in line:
            continue
        try:
            x, y, z = map(int, line.split(','))
            cubes.add((x, y, z))
        except ValueError:
            continue

    # All 6 directions: +/- x, y, z
    directions = [
        (1, 0, 0), (-1, 0, 0),
        (0, 1, 0), (0, -1, 0),
        (0, 0, 1), (0, 0, -1)
    ]

    # Count exposed faces
    exposed = 0
    for cube in cubes:
        x, y, z = cube
        for dx, dy, dz in directions:
            neighbor = (x + dx, y + dy, z + dz)
            if neighbor not in cubes:
                exposed += 1

    return exposed


def main():
    """Read from stdin and print result."""
    content = open(0).read().strip()
    result = solve(content)
    print(result)


if __name__ == "__main__":
    main()
