from icecream import ic
import sys

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
    floor_y = max_y + 2
    sand_count = 0

    def is_blocked(px, py):
        """Check if a position is blocked by rock or floor."""
        return py == floor_y or (px, py) in rocks

    while True:
        # Drop a unit of sand from (500, 0)
        x, y = 500, 0

        # Simulate falling
        while True:
            # Try moving down
            if not is_blocked(x, y + 1):
                y += 1
            # Try moving down-left
            elif not is_blocked(x - 1, y + 1):
                x -= 1
                y += 1
            # Try moving down-right
            elif not is_blocked(x + 1, y + 1):
                x += 1
                y += 1
            else:
                # Sand comes to rest
                rocks.add((x, y))
                sand_count += 1

                if x == 500 and y == 0:
                    return sand_count

                break


def main():
    """Read from stdin and print result."""
    content = open(0).read().strip()
    result = solve(content)
    print(result)


if __name__ == "__main__":
    main()
