from icecream import ic
import sys
from collections import deque
from math import gcd

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def solve(input_data):
    """Parse input and solve the puzzle."""
    lines = input_data.strip().split('\n')

    # Parse the grid
    grid = [list(line) for line in lines]
    rows = len(grid)
    cols = len(grid[0])

    # Remove walls from consideration (interior bounds)
    # Walls are at row 0, row rows-1, col 0, col cols-1
    inner_rows = rows - 2
    inner_cols = cols - 2

    # Parse blizzards (position, direction)
    blizzards = []
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            cell = grid[r][c]
            if cell in '^v<>':
                blizzards.append((r, c, cell))

    # Direction mappings
    directions = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1),
    }

    # Find cycle length (LCM of inner_rows and inner_cols)
    def lcm(a, b):
        return a * b // gcd(a, b)

    cycle_length = lcm(inner_rows, inner_cols)

    # Cache blizzard positions for each minute
    blizzard_cache = {}

    def get_blizzards_at_minute(minute):
        """Return set of blocked positions at given minute."""
        minute = minute % cycle_length
        if minute in blizzard_cache:
            return blizzard_cache[minute]

        blocked = set()
        for start_r, start_c, direction in blizzards:
            dr, dc = directions[direction]
            # Calculate position after 'minute' steps with wrapping
            new_r = start_r + dr * minute
            new_c = start_c + dc * minute

            # Wrap within inner bounds
            new_r = ((new_r - 1) % inner_rows) + 1
            new_c = ((new_c - 1) % inner_cols) + 1

            blocked.add((new_r, new_c))

        blizzard_cache[minute] = blocked
        return blocked

    # BFS to find shortest path
    # State: (row, col, minute % cycle_length)
    start = (0, 1)  # Starting position (entrance)
    goal = (rows - 1, cols - 2)  # Goal position (exit)

    queue = deque([(start[0], start[1], 0)])
    visited = set()
    visited.add((start[0], start[1], 0))

    # Movement options: up, down, left, right, wait
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]

    while queue:
        r, c, minute = queue.popleft()

        # Check if we reached the goal
        if (r, c) == goal:
            return minute

        # Get blizzard positions at next minute
        next_minute = minute + 1
        next_minute_mod = next_minute % cycle_length
        blocked = get_blizzards_at_minute(next_minute_mod)

        # Try all moves
        for dr, dc in moves:
            nr, nc = r + dr, c + dc

            # Check bounds (allow entrance and exit)
            if (nr, nc) == start or (nr, nc) == goal:
                # Can move to start/goal
                pass
            elif nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                # Out of bounds
                continue
            elif grid[nr][nc] == '#':
                # Wall
                continue

            # Check if this position is blocked by blizzard
            if (nr, nc) in blocked:
                continue

            # Check if already visited this state (use modulo for cycle detection)
            state = (nr, nc, next_minute_mod)
            if state not in visited:
                visited.add(state)
                queue.append((nr, nc, next_minute))

    return -1  # No solution found


def main():
    """Read from stdin and print result."""
    content = open(0).read().strip()
    result = solve(content)
    ic(result)


if __name__ == "__main__":
    main()
