def solve(input_data):
    lines = input_data.strip().split("\n")

    # Parse commands
    commands = []
    for line in lines:
        direction, steps = line.split()
        steps = int(steps)
        commands.append((direction, steps))

    # Direction vectors
    directions = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}

    # Initial positions (x, y)
    head = (0, 0)
    tail = (0, 0)
    tail_visited = {tail}

    for direction, steps in commands:
        dx, dy = directions[direction]
        for _ in range(steps):
            # Move head
            head = (head[0] + dx, head[1] + dy)

            # Check if tail needs to move
            hx, hy = head
            tx, ty = tail
            dist_x = abs(hx - tx)
            dist_y = abs(hy - ty)

            # If not touching, move tail one step closer to head
            if dist_x > 1 or dist_y > 1:
                new_tx = tx + (1 if hx > tx else -1 if hx < tx else 0)
                new_ty = ty + (1 if hy > ty else -1 if hy < ty else 0)
                tail = (new_tx, new_ty)
                tail_visited.add(tail)

    return len(tail_visited)


def main():
    content = open(0).read().strip()
    result = solve(content)
    print(result)


if __name__ == "__main__":
    main()
