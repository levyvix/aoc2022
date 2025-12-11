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

    # Initialize 10 knots, all at origin
    knots = [(0, 0) for _ in range(10)]
    tail_visited = {knots[9]}

    for direction, steps in commands:
        dx, dy = directions[direction]
        for _ in range(steps):
            # Move head
            knots[0] = (knots[0][0] + dx, knots[0][1] + dy)

            # Update each following knot
            for i in range(1, 10):
                leader_x, leader_y = knots[i - 1]
                follower_x, follower_y = knots[i]
                dist_x = abs(leader_x - follower_x)
                dist_y = abs(leader_y - follower_y)

                # If not touching, move follower one step closer to leader
                if dist_x > 1 or dist_y > 1:
                    new_x = follower_x + (
                        1
                        if leader_x > follower_x
                        else -1
                        if leader_x < follower_x
                        else 0
                    )
                    new_y = follower_y + (
                        1
                        if leader_y > follower_y
                        else -1
                        if leader_y < follower_y
                        else 0
                    )
                    knots[i] = (new_x, new_y)

            # Track knot 9 positions
            tail_visited.add(knots[9])

    return len(tail_visited)


def main():
    content = open(0).read().strip()
    result = solve(content)
    print(result)


if __name__ == "__main__":
    main()
