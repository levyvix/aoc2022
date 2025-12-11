from icecream import ic
import sys

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


# Rock shapes: list of (x, y) relative coordinates
ROCKS = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],  # -
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],  # +
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],  # L
    [(0, 0), (0, 1), (0, 2), (0, 3)],  # |
    [(0, 0), (1, 0), (0, 1), (1, 1)],  # square
]


def solve(input_data):
    """Parse input and solve the puzzle."""
    jets = input_data.strip()

    # Track occupied positions
    occupied = set()

    # Add floor
    for x in range(7):
        occupied.add((x, -1))

    max_height = 0
    jet_idx = 0

    for rock_num in range(2022):
        rock = ROCKS[rock_num % 5]

        # Start position: left edge 2 units from left, bottom 3 units above highest rock
        x = 2
        y = max_height + 3

        # Fall the rock
        while True:
            # Apply jet
            jet = jets[jet_idx % len(jets)]
            jet_idx += 1

            # Try to move left or right
            dx = -1 if jet == '<' else 1
            new_x = x + dx

            # Check if movement is valid
            can_move = True
            for rx, ry in rock:
                nx, ny = new_x + rx, y + ry
                if nx < 0 or nx >= 7 or (nx, ny) in occupied:
                    can_move = False
                    break

            if can_move:
                x = new_x

            # Try to fall
            new_y = y - 1
            can_fall = True
            for rx, ry in rock:
                nx, ny = x + rx, new_y + ry
                if (nx, ny) in occupied:
                    can_fall = False
                    break

            if can_fall:
                y = new_y
            else:
                # Rock stops here
                for rx, ry in rock:
                    occupied.add((x + rx, y + ry))
                max_height = max(max_height, y + max(ry for _, ry in rock) + 1)
                break

    return max_height


def main():
    """Read from stdin and print result."""
    content = open(0).read().strip()
    result = solve(content)
    ic(result)


if __name__ == "__main__":
    main()
