from collections import deque


def solve(input_data):
    """Parse input and solve the puzzle."""
    lines = input_data.strip().split("\n")

    grid = [list(line) for line in lines]
    rows = len(grid)
    cols = len(grid[0])

    # Find start and end positions
    start = None
    end = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                start = (r, c)
                grid[r][c] = "a"  # Treat S as 'a'
            elif grid[r][c] == "E":
                end = (r, c)
                grid[r][c] = "z"  # Treat E as 'z'

    # BFS to find shortest path
    queue = deque([(start, 0)])  # (position, distance)
    visited = {start}

    while queue:
        (r, c), dist = queue.popleft()

        if (r, c) == end:
            return dist

        # Try all 4 directions
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc

            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                # Can move if next elevation is at most 1 higher
                if ord(grid[nr][nc]) <= ord(grid[r][c]) + 1:
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
