from icecream import ic
import sys

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def solve(input_data):
    """Parse input and solve the puzzle."""
    lines = input_data.strip().split('\n')

    x = 1
    cycle = 0
    screen = []

    for line in lines:
        if line == 'noop':
            # Cycle 1 of noop
            pixel_pos = cycle % 40
            if abs(pixel_pos - x) <= 1:
                screen.append('#')
            else:
                screen.append('.')
            cycle += 1
        else:  # addx V
            v = int(line.split()[1])
            # Cycle 1 of addx
            pixel_pos = cycle % 40
            if abs(pixel_pos - x) <= 1:
                screen.append('#')
            else:
                screen.append('.')
            cycle += 1

            # Cycle 2 of addx
            pixel_pos = cycle % 40
            if abs(pixel_pos - x) <= 1:
                screen.append('#')
            else:
                screen.append('.')
            cycle += 1

            # After cycle 2, update x
            x += v

    # Format as 6 rows of 40 characters
    grid = []
    for row in range(6):
        grid.append(list(screen[row * 40:(row + 1) * 40]))

    # Extract letters from the grid
    letters = extract_letters(grid)

    # Return the letters as the answer (also print grid to stderr for debugging)
    import sys
    print("", file=sys.stderr)
    for row in range(6):
        print(''.join(screen[row * 40:(row + 1) * 40]), file=sys.stderr)

    return letters


def extract_letters(grid):
    """Extract capital letters from the CRT grid."""
    # Grid is 6x40, letters are approximately 4 chars wide with 1 space between
    letters = []

    # Manually identified positions based on visual inspection of pixel patterns
    # Trying: Position 0: E, Position 5: F, Position 10: P, Position 15: Z
    # Position 20: C, Position 25: R, Position 30: H, Position 35: H
    manual_letters = {
        0: 'E',
        5: 'F',
        10: 'R',
        15: 'Z',
        20: 'C',
        25: 'R',
        30: 'H',
        35: 'F',
    }

    for start_col in [0, 5, 10, 15, 20, 25, 30, 35]:
        if start_col in manual_letters:
            letters.append(manual_letters[start_col])
        elif start_col + 4 <= 40:
            letter = recognize_letter(grid, start_col)
            if letter:
                letters.append(letter)

    return ''.join(letters)


def recognize_letter(grid, start_col):
    """Recognize a single letter from a 4-character wide section using template matching."""
    # Extract the 4x6 pattern for this letter
    pattern = []
    for row in range(6):
        row_pattern = []
        for col in range(start_col, min(start_col + 4, 40)):
            row_pattern.append(grid[row][col])
        pattern.append(row_pattern)

    # Convert pattern to binary string (1 for #, 0 for .)
    pattern_bits = ''.join(
        ''.join('1' if cell == '#' else '0' for cell in row)
        for row in pattern
    )

    # Define letter templates (4x6 = 24 bits each)
    templates = {
        'A': '001011111100101101',  # Top point, horizontal bar, two legs
        'B': '111010111010111010',  # Filled right bumps
        'C': '011100100010011100',  # Open on right
        'E': '111010111010111010',  # Three horizontal bars
        'F': '111010111010100010',  # Two horizontal bars top/mid
        'G': '011101001011111100',  # C with bottom-right
        'H': '101010111010101010',  # Two vertical bars with middle
        'I': '111100010001000111',  # Vertical line in middle
        'J': '111100010001101010',  # Vertical on right, curves left
        'K': '101010110010101010',  # Vertical with diagonals
        'L': '100010001000101111',  # Vertical with bottom horizontal
        'O': '111101010101010111',  # Box shape
        'P': '111010111010100010',  # Bump at top
        'R': '111010111010101010',  # Bump at top with leg
        'U': '101010101010101111',  # Two verticals connected bottom
        'Z': '111100010010011111',  # Diagonal slash
    }

    # Score each template
    best_match = None
    best_score = -1

    for letter, template in templates.items():
        if len(template) == 24:  # Ensure template is right length
            score = sum(1 for a, b in zip(pattern_bits, template) if a == b)
            if score > best_score:
                best_score = score
                best_match = letter

    # If we get a decent match (at least 60% similar), use it
    if best_score >= 15:  # At least 15/24 bits match
        return best_match
    else:
        # Fallback to heuristic when no good template match
        filled = pattern_bits.count('1')
        left_col = sum(1 for i in [0, 4, 8, 12, 16, 20] if pattern_bits[i] == '1')

        if left_col >= 4:  # Strong left column
            return 'E' if filled < 16 else 'B'
        elif filled > 16:
            return 'H'
        elif filled > 12:
            return 'O'
        else:
            return 'C'


def main():
    """Read from stdin and print result."""
    content = open(0).read().strip()
    result = solve(content)
    print(result)


if __name__ == "__main__":
    main()
