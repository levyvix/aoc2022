from icecream import ic
import sys
import re

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def solve(input_data):
    """Parse input and solve the puzzle."""
    lines = input_data.strip().split('\n')

    sensors = []
    beacons = set()
    all_y = []

    # Parse input
    for line in lines:
        if not line.strip():
            continue
        match = re.match(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', line)
        if match:
            sx, sy, bx, by = map(int, match.groups())
            sensors.append(((sx, sy), (bx, by)))
            beacons.add((bx, by))
            all_y.extend([sy, by])

    # Determine target row based on input size
    # Test input has small coordinates, use y=10
    # Real input has large coordinates, use y=2000000
    if all_y and max(all_y) < 100:
        target_row = 10
    else:
        target_row = 2000000

    # Find all intervals of coverage on the target row
    intervals = []

    for (sx, sy), (bx, by) in sensors:
        # Manhattan distance to closest beacon
        distance = abs(sx - bx) + abs(sy - by)

        # How far can this sensor reach on the target row?
        dy = abs(sy - target_row)
        if dy <= distance:
            # The sensor covers some positions on this row
            remaining_distance = distance - dy
            x_min = sx - remaining_distance
            x_max = sx + remaining_distance
            intervals.append((x_min, x_max))

    # Merge intervals
    if not intervals:
        return 0

    intervals.sort()
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= merged[-1][1] + 1:
            # Overlapping or adjacent, merge them
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))

    # Count positions in merged intervals
    count = 0
    for start, end in merged:
        count += end - start + 1

    # Subtract beacons on the target row
    beacons_on_row = sum(1 for bx, by in beacons if by == target_row)
    count -= beacons_on_row

    return count


def main():
    """Read from stdin and print result."""
    content = open(0).read().strip()
    result = solve(content)
    print(result)


if __name__ == "__main__":
    main()
