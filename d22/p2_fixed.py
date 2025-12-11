from icecream import ic
import sys
import re

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def parse_input(content):
    map_str, path_str = content.split("\n\n")
    board = [list(row) for row in map_str.split("\n")]

    instructions = []
    parts = re.findall(r'(\d+)([RL]?)', path_str)
    for num, turn in parts:
        instructions.append((int(num), turn))
    return board, instructions


def find_start_position(board):
    for r_idx, row in enumerate(board):
        for c_idx, tile in enumerate(row):
            if tile == '.':
                return r_idx, c_idx
    return -1, -1


# Facing: 0=Right, 1=Down, 2=Left, 3=Up
dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]


def build_cube_transitions_example():
    """
    Build cube transition map for the example input.
    Returns dict: (face_id, edge_direction) -> (new_face_id, new_edge_direction, reversed)

    Edge directions: 0=Right, 1=Down, 2=Left, 3=Up
    """
    transitions = {}

    # Face 1 (Top)
    transitions[(1, 3)] = (2, 3, True)   # F1 Up -> F2 Top (reversed)
    transitions[(1, 2)] = (3, 3, False)  # F1 Left -> F3 Top
    transitions[(1, 0)] = (6, 3, True)   # F1 Right -> F6 Top (reversed)
    # F1 Down naturally connects to F4 Top (in the net)

    # Face 2 (Left)
    transitions[(2, 3)] = (1, 3, True)   # F2 Up -> F1 Top (reversed)
    transitions[(2, 2)] = (6, 1, True)   # F2 Left -> F6 Bottom (reversed)
    # F2 Right naturally connects to F3 Left (in the net)
    transitions[(2, 1)] = (5, 1, True)   # F2 Down -> F5 Bottom (reversed)

    # Face 3 (Front)
    transitions[(3, 3)] = (1, 2, False)  # F3 Up -> F1 Left
    # F3 Left naturally connects to F2 Right (in the net)
    # F3 Right naturally connects to F4 Left (in the net)
    transitions[(3, 1)] = (5, 2, True)   # F3 Down -> F5 Left (reversed)

    # Face 4 (Right)
    # F4 Up naturally connects to F1 Down (in the net)
    # F4 Left naturally connects to F3 Right (in the net)
    transitions[(4, 0)] = (6, 0, True)   # F4 Right -> F6 Right (reversed)
    # F4 Down naturally connects to F5 Top (in the net)

    # Face 5 (Bottom)
    # F5 Up naturally connects to F4 Down (in the net)
    transitions[(5, 2)] = (3, 1, True)   # F5 Left -> F3 Down (reversed)
    # F5 Right naturally connects to F6 Left (in the net)
    transitions[(5, 1)] = (2, 1, True)   # F5 Down -> F2 Down (reversed)

    # Face 6 (Back)
    transitions[(6, 3)] = (1, 0, True)   # F6 Up -> F1 Right (reversed)
    # F6 Left naturally connects to F5 Right (in the net)
    transitions[(6, 0)] = (4, 0, True)   # F6 Right -> F4 Right (reversed)
    transitions[(6, 1)] = (2, 2, True)   # F6 Down -> F2 Left (reversed)

    return transitions


def get_face_layout(is_example):
    """
    Returns face layout info.
    Format: {(face_row, face_col): (face_id, global_row, global_col)}
    """
    if is_example:
        face_size = 4
        layout = {
            (0, 2): (1, 0, 8),          # Face 1
            (1, 0): (2, 4, 0),          # Face 2
            (1, 1): (3, 4, 4),          # Face 3
            (1, 2): (4, 4, 8),          # Face 4
            (2, 2): (5, 8, 8),          # Face 5
            (2, 3): (6, 8, 12)          # Face 6
        }
    else:
        face_size = 50
        layout = {
            (0, 1): (1, 0, 50),         # Face 1
            (0, 2): (2, 0, 100),        # Face 2
            (1, 1): (3, 50, 50),        # Face 3
            (2, 0): (4, 100, 0),        # Face 4
            (2, 1): (5, 100, 50),       # Face 5
            (3, 0): (6, 150, 0)         # Face 6
        }
    return layout, face_size


def get_face_info(r, c, layout, face_size):
    """Get which face a position is on and local coordinates."""
    face_row = r // face_size
    face_col = c // face_size

    if (face_row, face_col) not in layout:
        return None, None, None

    face_id, start_r, start_c = layout[(face_row, face_col)]
    local_r = r - start_r
    local_c = c - start_c

    return face_id, local_r, local_c


def wrap_cube(r, c, facing, layout, face_size, transitions):
    """
    Handle wrapping when going off the edge of a face.
    Returns (new_r, new_c, new_facing)
    """
    face_id, local_r, local_c = get_face_info(r, c, layout, face_size)

    if face_id is None:
        raise ValueError(f"Position ({r}, {c}) not on any face")

    # Check if we have a cube transition for this edge
    if (face_id, facing) in transitions:
        new_face_id, new_edge, reversed_edge = transitions[(face_id, facing)]

        # Find the new face's global position
        new_face_pos = None
        for (fr, fc), (fid, gr, gc) in layout.items():
            if fid == new_face_id:
                new_face_pos = (gr, gc)
                break

        if new_face_pos is None:
            raise ValueError(f"New face {new_face_id} not found in layout")

        new_global_r, new_global_c = new_face_pos

        # Determine position along the current edge (0 to face_size-1)
        if facing == 0:  # Going right (leaving right edge)
            edge_pos = local_r
        elif facing == 1:  # Going down (leaving bottom edge)
            edge_pos = local_c
        elif facing == 2:  # Going left (leaving left edge)
            edge_pos = local_r
        else:  # facing == 3, going up (leaving top edge)
            edge_pos = local_c

        # Reverse if needed
        if reversed_edge:
            edge_pos = face_size - 1 - edge_pos

        # Map to new face edge
        # new_edge tells us which edge we're entering (0=right, 1=down, 2=left, 3=up)
        if new_edge == 0:  # Entering from right edge
            new_local_r = edge_pos
            new_local_c = face_size - 1
            new_facing = 2  # Now facing left
        elif new_edge == 1:  # Entering from bottom edge
            new_local_r = face_size - 1
            new_local_c = edge_pos
            new_facing = 3  # Now facing up
        elif new_edge == 2:  # Entering from left edge
            new_local_r = edge_pos
            new_local_c = 0
            new_facing = 0  # Now facing right
        else:  # new_edge == 3, entering from top edge
            new_local_r = 0
            new_local_c = edge_pos
            new_facing = 1  # Now facing down

        return new_global_r + new_local_r, new_global_c + new_local_c, new_facing

    else:
        # No special transition, this is a natural edge in the net
        # Just continue in the same direction
        return r + dr[facing], c + dc[facing], facing


def solve_part2(input_data):
    board, instructions = parse_input(input_data)

    max_row = len(board)
    max_col_len = max(len(row) for row in board)

    # Pad board to rectangular grid
    grid = []
    for row in board:
        grid.append(list(row) + [' '] * (max_col_len - len(row)))

    # Determine if example or real input
    is_example = (max_col_len == 16 and max_row == 12)

    layout, face_size = get_face_layout(is_example)
    transitions = build_cube_transitions_example() if is_example else {}

    current_r, current_c = find_start_position(grid)
    facing = 0  # Start facing right

    ic(f"Starting at ({current_r}, {current_c}), facing {facing}")

    for num_steps, turn_direction in instructions:
        ic(f"Moving {num_steps} steps, then turning {turn_direction}")

        for step in range(num_steps):
            # Try to move one step
            next_r = current_r + dr[facing]
            next_c = current_c + dc[facing]
            next_facing = facing

            # Check if we're going off a face
            if (0 <= next_r < len(grid) and
                0 <= next_c < len(grid[0]) and
                grid[next_r][next_c] != ' '):
                # Still on the board, no wrapping needed
                pass
            else:
                # Need to wrap
                next_r, next_c, next_facing = wrap_cube(
                    current_r, current_c, facing, layout, face_size, transitions
                )

            # Check if we hit a wall
            if grid[next_r][next_c] == '#':
                ic(f"  Hit wall at ({next_r}, {next_c}), stopping")
                break
            elif grid[next_r][next_c] == '.':
                current_r, current_c, facing = next_r, next_c, next_facing
                ic(f"  Step {step+1}: now at ({current_r}, {current_c}), facing {facing}")
            else:
                raise ValueError(f"Invalid tile at ({next_r}, {next_c}): {grid[next_r][next_c]}")

        # Handle turning
        if turn_direction == 'R':
            facing = (facing + 1) % 4
        elif turn_direction == 'L':
            facing = (facing - 1 + 4) % 4

        ic(f"After turn: facing {facing}")

    # Password calculation (1-indexed)
    password = 1000 * (current_r + 1) + 4 * (current_c + 1) + facing
    ic(f"Final: row={current_r+1}, col={current_c+1}, facing={facing}")
    ic(f"Password: {password}")

    return password


def main():
    content = open(0).read()
    result = solve_part2(content)
    print(result)


if __name__ == "__main__":
    main()
