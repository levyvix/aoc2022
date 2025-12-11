from icecream import ic
import sys
from collections import deque

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def solve(input_data):
    """Parse input and solve the puzzle."""
    lines = input_data.strip().split('\n')

    grid = [list(line) for line in lines]
    rows = len(grid)
    cols = len(grid[0])

    # Find start and end positions
    start = None
    end = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start = (r, c)
                grid[r][c] = 'a'
            elif grid[r][c] == 'E':
                end = (r, c)
                grid[r][c] = 'z'

    # BFS backwards from E to find shortest path to any 'a'
    queue = deque([(end, 0)])  # (position, distance)
    visited = {end}

    while queue:
        (r, c), dist = queue.popleft()

        # Check if we reached an 'a'
        if grid[r][c] == 'a':
            return dist

        # Try all 4 directions
        # Backward rule: can move to adjacent position if it's at least 1 lower (or any height higher)
        # Equivalently: next_elevation >= current_elevation - 1
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc

            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                # Can move if next elevation is at least 1 lower
                if ord(grid[nr][nc]) >= ord(grid[r][c]) - 1:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), dist + 1))

    return -1  # No path found


def main():
    """Read from stdin and print result."""
    content = open(0).read().strip()
    result = solve(content)
    print(result)


if __name__ == "__main__":
    main()
