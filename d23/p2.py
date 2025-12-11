from icecream import ic
import sys
from collections import defaultdict

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def solve(input_data):
    """Parse input and solve the puzzle."""
    lines = input_data.strip().split('\n')

    # Parse elves positions
    elves = set()
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == '#':
                elves.add((r, c))

    # Direction deltas: N, S, W, E
    directions = {
        'N': (-1, 0),
        'S': (1, 0),
        'W': (0, -1),
        'E': (0, 1),
    }

    # Adjacent positions to check for each direction
    adjacent_for_dir = {
        'N': [(-1, -1), (-1, 0), (-1, 1)],
        'S': [(1, -1), (1, 0), (1, 1)],
        'W': [(-1, -1), (0, -1), (1, -1)],
        'E': [(-1, 1), (0, 1), (1, 1)],
    }

    # All 8 adjacent positions
    all_adjacent = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]

    # Direction order (will rotate)
    dir_order = ['N', 'S', 'W', 'E']

    # Run until no elves move
    round_num = 0
    while True:
        round_num += 1

        # Phase 1: Each elf proposes a move
        proposals = {}  # elf_pos -> proposed_pos

        for elf in elves:
            r, c = elf

            # Check if any adjacent elf exists
            has_neighbor = False
            for dr, dc in all_adjacent:
                if (r + dr, c + dc) in elves:
                    has_neighbor = True
                    break

            # If no neighbors, don't move
            if not has_neighbor:
                continue

            # Try each direction in order
            proposed = None
            for direction in dir_order:
                # Check if this direction is clear
                clear = True
                for dr, dc in adjacent_for_dir[direction]:
                    if (r + dr, c + dc) in elves:
                        clear = False
                        break

                if clear:
                    dr, dc = directions[direction]
                    proposed = (r + dr, c + dc)
                    break

            if proposed:
                proposals[elf] = proposed

        # If no proposals, we're done
        if not proposals:
            return round_num

        # Phase 2: Move elves if they're the only one proposing that position
        proposal_count = defaultdict(list)
        for elf, target in proposals.items():
            proposal_count[target].append(elf)

        # Move elves with unique proposals
        for target, elves_proposing in proposal_count.items():
            if len(elves_proposing) == 1:
                elf = elves_proposing[0]
                elves.remove(elf)
                elves.add(target)

        # Rotate direction order
        dir_order.append(dir_order.pop(0))


def main():
    """Read from stdin and print result."""
    content = open(0).read().strip()
    result = solve(content)
    ic(result)


if __name__ == "__main__":
    main()
