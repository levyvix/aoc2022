import re


def parse_input(content):
    map_str, path_str = content.split("\n\n")
    board = [list(row) for row in map_str.split("\n")]

    instructions = []
    # Split path_str into numbers and turns (e.g., "10R5L" -> ["10", "R", "5", "L"])
    # This regex is correct: (\d+) captures numbers, ([RL]?) captures optional R or L
    parts = re.findall(r"(\d+)([RL]?)", path_str)
    for num, turn in parts:
        instructions.append((int(num), turn))
    return board, instructions


def find_start_position(board):
    for r_idx, row in enumerate(board):
        for c_idx, tile in enumerate(row):
            if tile == ".":
                return r_idx, c_idx
    return -1, -1  # Should not happen


def solve(input_data):
    board, instructions = parse_input(input_data)

    max_row = len(board)
    max_col_len = max(len(row) for row in board)

    # Pad board for easier boundary checks, fill with ' ' where no tile
    # Using ' ' to denote empty space not part of the active map.
    grid = []
    for row in board:
        grid.append(row + [" "] * (max_col_len - len(row)))

    # Facing: 0=Right, 1=Down, 2=Left, 3=Up
    dr = [0, 1, 0, -1]  # Delta row
    dc = [1, 0, -1, 0]  # Delta col

    current_r, current_c = find_start_position(grid)
    facing = 0  # Start facing right

    for num_steps, turn_direction in instructions:
        for _ in range(num_steps):
            next_r, next_c = current_r + dr[facing], current_c + dc[facing]

            # Determine the effective width and height of the map, considering irregular shape
            # Find the actual boundaries for the current row/column for wrapping
            wrap_target_r, wrap_target_c = -1, -1

            # Check if next step is out of bounds or into empty space
            if (
                not (0 <= next_r < max_row and 0 <= next_c < max_col_len)
                or grid[next_r][next_c] == " "
            ):
                # Need to wrap
                if facing == 0:  # Moving Right
                    # Find first non-' ' tile in the current row from left
                    for c_check in range(max_col_len):
                        if grid[current_r][c_check] != " ":
                            wrap_target_r, wrap_target_c = current_r, c_check
                            break
                elif facing == 1:  # Moving Down
                    # Find first non-' ' tile in the current column from top
                    for r_check in range(max_row):
                        if (
                            current_c < len(grid[r_check])
                            and grid[r_check][current_c] != " "
                        ):
                            wrap_target_r, wrap_target_c = r_check, current_c
                            break
                elif facing == 2:  # Moving Left
                    # Find first non-' ' tile in the current row from right
                    for c_check in range(max_col_len - 1, -1, -1):
                        if grid[current_r][c_check] != " ":
                            wrap_target_r, wrap_target_c = current_r, c_check
                            break
                elif facing == 3:  # Moving Up
                    # Find first non-' ' tile in the current column from bottom
                    for r_check in range(max_row - 1, -1, -1):
                        if (
                            current_c < len(grid[r_check])
                            and grid[r_check][current_c] != " "
                        ):
                            wrap_target_r, wrap_target_c = r_check, current_c
                            break

                next_r, next_c = wrap_target_r, wrap_target_c

            # Now, next_r, next_c should be a valid tile ('.' or '#')
            if grid[next_r][next_c] == "#":
                break  # Hit a wall, stop moving for this instruction
            elif grid[next_r][next_c] == ".":
                current_r, current_c = next_r, next_c
            # If it's a space, something is wrong with the wrapping logic.

        # Handle turning
        if turn_direction == "R":
            facing = (facing + 1) % 4
        elif turn_direction == "L":
            facing = (facing - 1 + 4) % 4

    # Password calculation: 1000 * row + 4 * column + facing
    # Rows and columns are 1-indexed
    final_password = 1000 * (current_r + 1) + 4 * (current_c + 1) + facing
    return final_password


def main():
    content = open(0).read()
    result = solve(content)
    print(result)


if __name__ == "__main__":
    main()
