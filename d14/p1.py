from icecream import ic
import sys
from collections import deque

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def solve(input_data):
    """Parse input and solve the puzzle."""
    lines = input_data.strip().split('\n')

    # Parse rock paths
    rocks = set()
    for line in lines:
        points = line.split(' -> ')
        coords = [tuple(map(int, p.split(','))) for p in points]

        for i in range(len(coords) - 1):
            x1, y1 = coords[i]
            x2, y2 = coords[i + 1]

            # Draw line from (x1,y1) to (x2,y2)
            if x1 == x2:  # Vertical line
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    rocks.add((x1, y))
            else:  # Horizontal line
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    rocks.add((x, y1))

    max_y = max(y for x, y in rocks)
    sand_count = 0

    while True:
        # Drop a unit of sand from (500, 0)
        x, y = 500, 0

        # Simulate falling
        while True:
            if y > max_y:
                # Sand fell into the abyss
                return sand_count

            # Try moving down
            if (x, y + 1) not in rocks:
                y += 1
            # Try moving down-left
            elif (x - 1, y + 1) not in rocks:
                x -= 1
                y += 1
            # Try moving down-right
            elif (x + 1, y + 1) not in rocks:
                x += 1
                y += 1
            else:
                # Sand comes to rest
                rocks.add((x, y))
                sand_count += 1
                break


def main():
    """Read from stdin and print result."""
    content = open(0).read().strip()
    result = solve(content)
    print(result)


if __name__ == "__main__":
    main()
