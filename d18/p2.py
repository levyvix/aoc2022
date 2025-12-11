from icecream import ic
import sys
from collections import deque

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def solve(input_data):
    """Count only exterior surface area using flood fill."""
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

    # Find bounds
    xs = [x for x, y, z in cubes]
    ys = [y for x, y, z in cubes]
    zs = [z for x, y, z in cubes]

    min_x, max_x = min(xs) - 1, max(xs) + 1
    min_y, max_y = min(ys) - 1, max(ys) + 1
    min_z, max_z = min(zs) - 1, max(zs) + 1

    # Flood fill from outside to mark all reachable exterior spaces
    exterior = set()
    queue = deque([(min_x, min_y, min_z)])
    exterior.add((min_x, min_y, min_z))

    directions = [
        (1, 0, 0), (-1, 0, 0),
        (0, 1, 0), (0, -1, 0),
        (0, 0, 1), (0, 0, -1)
    ]

    while queue:
        x, y, z = queue.popleft()

        for dx, dy, dz in directions:
            nx, ny, nz = x + dx, y + dy, z + dz

            # Check bounds and if not visited
            if (min_x <= nx <= max_x and
                min_y <= ny <= max_y and
                min_z <= nz <= max_z and
                (nx, ny, nz) not in exterior and
                (nx, ny, nz) not in cubes):

                exterior.add((nx, ny, nz))
                queue.append((nx, ny, nz))

    # Count exposed faces only touching exterior
    exposed = 0
    for cube in cubes:
        x, y, z = cube
        for dx, dy, dz in directions:
            neighbor = (x + dx, y + dy, z + dz)
            if neighbor in exterior:
                exposed += 1

    return exposed


def main():
    """Read from stdin and print result."""
    content = open(0).read().strip()
    result = solve(content)
    print(result)


if __name__ == "__main__":
    main()
