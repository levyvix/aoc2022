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
    target_rocks = 1000000000000

    occupied = set()
    for x in range(7):
        occupied.add((x, -1))

    max_height = 0
    jet_idx = 0
    heights_at = [0] * 7  # Track height per column
    height_offset = 0  # Track height from skipped cycles

    # For cycle detection: (rock_type, jet_idx % len(jets), height_profile) -> (rock_num, max_height)
    states = {}
    rock_num = 0

    while rock_num < target_rocks:
        rock_type = rock_num % 5
        jet_position = jet_idx % len(jets)

        # Create state key based on rock type, jet position, and relative height profile
        max_h = max_height
        height_profile = tuple(max_h - h for h in heights_at)

        state_key = (rock_type, jet_position, height_profile)

        if state_key in states:
            # Found a cycle
            prev_rock_num, prev_max_height = states[state_key]
            cycle_length = rock_num - prev_rock_num
            height_gain = max_height - prev_max_height

            # How many complete cycles can we skip?
            remaining = target_rocks - rock_num
            complete_cycles = remaining // cycle_length

            # Add height from complete cycles
            height_offset += complete_cycles * height_gain
            rock_num += complete_cycles * cycle_length

            if rock_num >= target_rocks:
                return max_height + height_offset

            # Continue simulation for the remainder
            # Don't prune - keep all occupied cells to maintain consistency
            states.clear()

        states[state_key] = (rock_num, max_height)

        rock = ROCKS[rock_type]
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
                    heights_at[x + rx] = max(heights_at[x + rx], y + ry + 1)
                max_height = max(max_height, y + max(ry for _, ry in rock) + 1)
                break

        rock_num += 1

    return max_height + height_offset


def main():
    """Read from stdin and print result."""
    content = open(0).read().strip()
    result = solve(content)
    ic(result)


if __name__ == "__main__":
    main()
