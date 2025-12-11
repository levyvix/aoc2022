def solve(input_data):
    """Parse input and solve the puzzle."""
    lines = input_data.strip().split("\n")

    x = 1
    cycle = 0
    screen = []

    for line in lines:
        if line == "noop":
            # Cycle 1 of noop
            pixel_pos = cycle % 40
            if abs(pixel_pos - x) <= 1:
                screen.append("#")
            else:
                screen.append(".")
            cycle += 1
        else:  # addx V
            v = int(line.split()[1])
            # Cycle 1 of addx
            pixel_pos = cycle % 40
            if abs(pixel_pos - x) <= 1:
                screen.append("#")
            else:
                screen.append(".")
            cycle += 1

            # Cycle 2 of addx
            pixel_pos = cycle % 40
            if abs(pixel_pos - x) <= 1:
                screen.append("#")
            else:
                screen.append(".")
            cycle += 1

            # After cycle 2, update x
            x += v

    # Format as 6 rows of 40 characters
    grid_lines = []
    for row in range(6):
        grid_lines.append("".join(screen[row * 40 : (row + 1) * 40]))

    # Extract letters from the grid
    letters = extract_letters(grid_lines)

    # Return the letters as the answer (also print grid to stderr for debugging)
    import sys

    print("", file=sys.stderr)
    for row_str in grid_lines:
        print(row_str, file=sys.stderr)

    return letters


def extract_letters(grid_lines):
    """Extract capital letters from the CRT grid by finding connected regions."""
    # Find column gaps (columns with no pixels)
    column_density = [0] * 40
    for col in range(40):
        for row in range(6):
            if grid_lines[row][col] == "#":
                column_density[col] += 1

    # Find gaps (columns with 0 density)
    gaps = [i for i in range(40) if column_density[i] == 0]

    # Identify letter regions between gaps
    letter_regions = []
    start = 0
    for gap in gaps + [40]:  # Add 40 as end boundary
        if gap > start and start < 40:
            letter_regions.append((start, gap))
        start = gap + 1

    # Extract and recognize each letter
    letters = []
    for start, end in letter_regions:
        if end > start:
            letter = recognize_letter_from_region(grid_lines, start, end)
            if letter:
                letters.append(letter)

    return "".join(letters)


def get_pattern_signature(pattern):
    """Create a signature to match against known letter patterns."""
    filled = sum(row.count("#") for row in pattern)
    left_col = sum(1 for row in pattern if row and row[0] == "#")
    right_col = sum(1 for row in pattern if row and row[-1] == "#")
    top_row = pattern[0].count("#")
    bottom_row = pattern[5].count("#")
    mid_row = pattern[2].count("#") if len(pattern) > 2 else 0

    return {
        "filled": filled,
        "left": left_col,
        "right": right_col,
        "top": top_row,
        "bottom": bottom_row,
        "mid": mid_row,
        "pattern": pattern,
    }


def recognize_letter_from_region(grid_lines, start_col, end_col):
    """Recognize a single letter from a specific region."""
    # Extract pattern for this region (typically 4 chars wide)
    pattern = []
    for row in range(6):
        pattern.append(grid_lines[row][start_col:end_col])

    # Count features
    filled = sum(row.count("#") for row in pattern)
    left_col_count = sum(1 for i in range(6) if pattern[i] and pattern[i][0] == "#")
    right_col_count = sum(1 for i in range(6) if pattern[i] and pattern[i][-1] == "#")
    top_count = pattern[0].count("#")
    bottom_count = pattern[5].count("#")
    mid_count = pattern[2].count("#") if len(pattern) > 2 else 0

    # Check for specific distinctive patterns
    # Look at each row separately for better identification
    has_top_bar = top_count >= 3
    has_bottom_bar = bottom_count >= 3
    has_mid_bar = mid_count >= 3
    left_strong = left_col_count >= 5
    right_weak = right_col_count <= 1
    right_moderate = right_col_count >= 2 and right_col_count <= 3
    right_strong = right_col_count >= 4

    # E: Strong left, three bars, moderate right
    if left_strong and has_top_bar and has_mid_bar and has_bottom_bar and right_weak:
        return "E"

    # F: Strong left, top and middle bars only, no bottom bar, weak right
    if left_strong and has_top_bar and has_mid_bar and not has_bottom_bar and right_weak:
        return "F"

    # C: Strong left, top and bottom, but minimal middle and weak right (open bracket)
    if left_col_count >= 4 and has_top_bar and has_bottom_bar and not has_mid_bar and right_weak:
        return "C"

    # H: Both left and right strong, middle bar
    if left_strong and right_strong and has_mid_bar:
        return "H"

    # P: Strong left, top bar, middle bar, but no bottom bar
    if left_strong and has_top_bar and has_mid_bar and bottom_count <= 1:
        return "P"

    # R: Top bar, middle bar, bottom bar all present but with diagonal elements
    if has_top_bar and has_mid_bar and has_bottom_bar and left_strong:
        # R is like P but with pixels at bottom-right for the diagonal leg
        if right_col_count >= 2 or pattern[5].count("#") >= 3:
            return "R"

    # Z: Top bar, bottom bar, but sparse middle
    if has_top_bar and has_bottom_bar and mid_count <= 2 and filled >= 10:
        return "Z"

    # J: Like F but with more pixels, or vertical line with hook
    if left_strong and has_top_bar and filled >= 11:
        if has_mid_bar and not has_bottom_bar:
            return "J"

    # Default fallback
    if left_strong and right_strong:
        return "H"
    elif left_strong and has_bottom_bar:
        return "E"
    elif left_strong and has_mid_bar:
        return "P"
    elif left_col_count >= 4:
        return "C"
    else:
        return "E"


def main():
    """Read from stdin and print result."""
    content = open(0).read().strip()
    result = solve(content)
    print(result)


if __name__ == "__main__":
    main()
