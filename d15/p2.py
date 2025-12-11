from icecream import ic
import sys
import re

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def solve(input_data):
    """Parse input and solve the puzzle."""
    lines = input_data.strip().split('\n')

    sensors = []
    all_y = []

    # Parse input
    for line in lines:
        if not line.strip():
            continue
        match = re.match(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', line)
        if match:
            sx, sy, bx, by = map(int, match.groups())
            sensors.append(((sx, sy), (bx, by)))
            all_y.extend([sy, by])

    # Determine search bounds based on input size
    if all_y and max(all_y) < 100:
        max_coord = 20
    else:
        max_coord = 4000000

    # For each y coordinate, find gaps in sensor coverage
    for y in range(max_coord + 1):
        # Find all intervals of coverage on this row
        intervals = []

        for (sx, sy), (bx, by) in sensors:
            # Manhattan distance to closest beacon
            distance = abs(sx - bx) + abs(sy - by)

            # How far can this sensor reach on this row?
            dy = abs(sy - y)
            if dy <= distance:
                # The sensor covers some positions on this row
                remaining_distance = distance - dy
                x_min = sx - remaining_distance
                x_max = sx + remaining_distance
                intervals.append((x_min, x_max))

        if not intervals:
            # No coverage on this row, beacon could be anywhere
            return y  # But we need to find x too, shouldn't happen

        # Merge intervals
        intervals.sort()
        merged = [intervals[0]]

        for start, end in intervals[1:]:
            if start <= merged[-1][1] + 1:
                # Overlapping or adjacent, merge them
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            else:
                merged.append((start, end))

        # Check for gap in coverage within [0, max_coord]
        # Check before first interval
        if merged[0][0] > 0:
            x = 0
            return x * 4000000 + y

        # Check between intervals
        for i in range(len(merged) - 1):
            gap_start = merged[i][1] + 1
            gap_end = merged[i + 1][0] - 1
            if gap_start <= gap_end and gap_start <= max_coord:
                x = gap_start
                return x * 4000000 + y

        # Check after last interval
        if merged[-1][1] < max_coord:
            x = merged[-1][1] + 1
            return x * 4000000 + y

    return 0


def main():
    """Read from stdin and print result."""
    content = open(0).read().strip()
    result = solve(content)
    print(result)


if __name__ == "__main__":
    main()
