from icecream import ic
import sys
import re

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))

def parse_input(content):
    map_str, path_str = content.split("\n\n")
    board = [list(row) for row in map_str.split("\n")]
    # ic(f"Raw map_str lines: {[len(row) for row in map_str.split('                ')]}")

    instructions = []
    # Split path_str into numbers and turns (e.g., "10R5L" -> ["10", "R", "5", "L"])
    parts = re.findall(r'(\d+)([RL]?)', path_str)
    for num, turn in parts:
        instructions.append((int(num), turn))
    return board, instructions

def find_start_position(board):
    for r_idx, row in enumerate(board):
        for c_idx, tile in enumerate(row):
            if tile == '.':
                return r_idx, c_idx
    return -1, -1 # Should not happen

# Facing: 0=Right, 1=Down, 2=Left, 3=Up
dr = [0, 1, 0, -1] # Delta row
dc = [1, 0, -1, 0] # Delta col

def get_face_info(r, c, face_size, is_example):
    if is_example:
        # Example faces based on the 1111...6666 diagram
        # (face_row_idx, face_col_idx): (face_id, global_start_r, global_start_c)
        faces_map = {
            (0, 2): (1, 0, 2 * face_size),         # Face 1
            (1, 0): (2, 1 * face_size, 0),         # Face 2
            (1, 1): (3, 1 * face_size, 1 * face_size), # Face 3
            (1, 2): (4, 1 * face_size, 2 * face_size), # Face 4
            (2, 2): (5, 2 * face_size, 2 * face_size), # Face 5
            (2, 3): (6, 2 * face_size, 3 * face_size)  # Face 6
        }
    else:
        # Real input layout (50x50 faces)
        faces_map = {
            (0, 1): (1, 0, 1 * face_size),         # Face 1
            (1, 0): (2, 1 * face_size, 0),         # Face 2
            (1, 1): (3, 1 * face_size, 1 * face_size), # Face 3
            (1, 2): (4, 1 * face_size, 2 * face_size), # Face 4
            (2, 2): (5, 2 * face_size, 2 * face_size), # Face 5
            (3, 0): (6, 3 * face_size, 0)          # Face 6
        }
    
    face_row_idx = r // face_size
    face_col_idx = c // face_size
    current_face_key = (face_row_idx, face_col_idx)

    if current_face_key in faces_map:
        face_id, start_r, start_c = faces_map[current_face_key]
        local_r = r - start_r
        local_c = c - start_c
        return face_id, local_r, local_c, start_r, start_c
    return -1, -1, -1, -1, -1 # Not on a defined face

def get_cube_wrap_coordinates(r, c, facing, face_size, is_example):
    # Determine which face we are on and convert to local coordinates
    face_id, local_r, local_c, start_r, start_c = get_face_info(r, c, face_size, is_example)
    
    if face_id == -1:
        raise ValueError(f"get_cube_wrap_coordinates: Global coordinates ({r}, {c}) not on a defined face.")

    new_r, new_c, new_facing = -1, -1, -1

    if is_example:
        # Based on common interpretation of the example cube net
        if face_id == 1: # Face 1 (0,2)
            if facing == 3: # Up (local_r=0) -> F2 Left edge
                new_r = faces_config[(1,0)][1] + local_c
                new_c = faces_config[(1,0)][2]
                new_facing = 1 # Down
            elif facing == 2: # Left (local_c=0) -> F3 Top edge
                new_r = faces_config[(1,1)][1]
                new_c = faces_config[(1,1)][2] + local_r
                new_facing = 1 # Down
            elif facing == 0: # Right (local_c=face_size-1) -> F4 Left edge
                new_r = faces_config[(1,2)][1] + local_r
                new_c = faces_config[(1,2)][2]
                new_facing = 0 # Right
            elif facing == 1: # Down (local_r=face_size-1) -> F3 Top edge
                new_r = faces_config[(1,1)][1]
                new_c = faces_config[(1,1)][2] + local_c
                new_facing = 1 # Down
        elif face_id == 2: # Face 2 (1,0)
            if facing == 3: # Up (local_r=0) -> F1 Left edge (inverted)
                new_r = faces_config[(0,2)][1] + (face_size - 1 - local_c)
                new_c = faces_config[(0,2)][2]
                new_facing = 0 # Right
            elif facing == 2: # Left (local_c=0) -> F5 Top edge (inverted)
                new_r = faces_config[(2,2)][1] + (face_size - 1 - local_r)
                new_c = faces_config[(2,2)][2]
                new_facing = 0 # Right
            elif facing == 0: # Right (local_c=face_size-1) -> F3 Left edge
                new_r = faces_config[(1,1)][1] + local_r
                new_c = faces_config[(1,1)][2]
                new_facing = 0 # Right
            elif facing == 1: # Down (local_r=face_size-1) -> F5 Left edge (inverted)
                new_r = faces_config[(2,2)][1] + (face_size - 1 - local_r)
                new_c = faces_config[(2,2)][2] + local_c
                new_facing = 3 # Up
        elif face_id == 3: # Face 3 (1,1)
            if facing == 3: # Up (local_r=0) -> F1 Bottom edge
                new_r = faces_config[(0,2)][1] + (face_size - 1)
                new_c = faces_config[(0,2)][2] + local_c
                new_facing = 3 # Up
            elif facing == 2: # Left (local_c=0) -> F2 Right edge
                new_r = faces_config[(1,0)][1] + local_r
                new_c = faces_config[(1,0)][2] + (face_size - 1)
                new_facing = 2 # Left
            elif facing == 0: # Right (local_c=face_size-1) -> F4 Left edge
                new_r = faces_config[(1,2)][1] + local_r
                new_c = faces_config[(1,2)][2]
                new_facing = 0 # Right
            elif facing == 1: # Down (local_r=face_size-1) -> F5 Top edge
                new_r = faces_config[(2,2)][1] + local_c
                new_c = faces_config[(2,2)][2]
                new_facing = 1 # Down
        elif face_id == 4: # Face 4 (1,2)
            if facing == 3: # Up (local_r=0) -> F1 Right edge (inverted)
                new_r = faces_config[(0,2)][1] + (face_size - 1 - local_c)
                new_c = faces_config[(0,2)][2] + (face_size - 1)
                new_facing = 2 # Left
            elif facing == 2: # Left (local_c=0) -> F3 Right edge
                new_r = faces_config[(1,1)][1] + local_r
                new_c = faces_config[(1,1)][2] + (face_size - 1)
                new_facing = 2 # Left
            elif facing == 0: # Right (local_c=face_size-1) -> F6 Left edge (inverted)
                new_r = faces_config[(2,3)][1] + (face_size - 1 - local_r)
                new_c = faces_config[(2,3)][2]
                new_facing = 0 # Right
            elif facing == 1: # Down (local_r=face_size-1) -> F5 Top edge
                new_r = faces_config[(2,2)][1] + local_c
                new_c = faces_config[(2,2)][2]
                new_facing = 1 # Down
        elif face_id == 5: # Face 5 (2,2)
            if facing == 3: # Up (local_r=0) -> F4 Bottom edge
                new_r = faces_config[(1,2)][1] + (face_size - 1)
                new_c = faces_config[(1,2)][2] + local_c
                new_facing = 3 # Up
            elif facing == 2: # Left (local_c=0) -> F2 Bottom edge (inverted)
                new_r = faces_config[(1,0)][1] + (face_size - 1)
                new_c = faces_config[(1,0)][2] + (face_size - 1 - local_r)
                new_facing = 3 # Up
            elif facing == 0: # Right (local_c=face_size-1) -> F6 Top edge
                new_r = faces_config[(2,3)][1]
                new_c = faces_config[(2,3)][2] + local_r
                new_facing = 1 # Down
            elif facing == 1: # Down (local_r=face_size-1) -> F6 Left edge (inverted)
                new_r = faces_config[(2,3)][1] + local_c
                new_c = faces_config[(2,3)][2]
                new_facing = 0 # Right
        elif face_id == 6: # Face 6 (2,3)
            if facing == 3: # Up (local_r=0) -> F4 Right edge (inverted)
                new_r = faces_config[(1,2)][1] + (face_size - 1 - local_c)
                new_c = faces_config[(1,2)][2] + (face_size - 1)
                new_facing = 2 # Left
            elif facing == 2: # Left (local_c=0) -> F5 Right edge
                new_r = faces_config[(2,2)][1] + local_r
                new_c = faces_config[(2,2)][2] + (face_size - 1)
                new_facing = 2 # Left
            elif facing == 0: # Right (local_c=face_size-1) -> F1 Bottom edge (inverted)
                new_r = faces_config[(0,2)][1] + (face_size - 1 - local_r)
                new_c = faces_config[(0,2)][2] + (face_size - 1)
                new_facing = 3 # Up
            elif facing == 1: # Down (local_r=face_size-1) -> F2 Left edge
                new_r = faces_config[(1,0)][1] + local_c
                new_c = faces_config[(1,0)][2]
                new_facing = 1 # Down
    
    # Real input-specific transitions
    else:
        # Face 1: (0, 1) in face_idx coordinates -> Global (0, 50) to (49, 99)
        if face_id == 1:
            if facing == 3: # Up (local_r=0) -> F6
                new_r = faces_config[(3,0)][1] + local_c # F6_start_r + local_c
                new_c = faces_config[(3,0)][2] + 0       # F6_start_c + 0 (left edge)
                new_facing = 0 # Right
            elif facing == 2: # Left (local_c=0) -> F4
                new_r = faces_config[(2,0)][1] + 0 # F4_start_r + 0 (top edge)
                new_c = faces_config[(2,0)][2] + (face_size - 1 - local_r) # F4_start_c + (S - 1 - local_r)
                new_facing = 0 # Right
            elif facing == 0: # Right (local_c=face_size-1) -> F2
                new_r = faces_config[(0,2)][1] + local_r
                new_c = faces_config[(0,2)][2] + 0
                new_facing = 0 # Right
            elif facing == 1: # Down (local_r=face_size-1) -> F3
                new_r = faces_config[(1,1)][1] + 0
                new_c = faces_config[(1,1)][2] + local_c
                new_facing = 1 # Down

        # Face 2: (1, 0) in face_idx coordinates
        elif face_id == 2:
            if facing == 3: # Up (local_r=0) -> F1 Left edge
                new_r = faces_config[(0,1)][1] + (face_size - 1 - local_c)
                new_c = faces_config[(0,1)][2]
                new_facing = 0 # Right
            elif facing == 2: # Left (local_c=0) -> F6 Left edge
                new_r = faces_config[(3,0)][1] + (face_size - 1 - local_r)
                new_c = faces_config[(3,0)][2]
                new_facing = 0 # Right
            elif facing == 0: # Right (local_c=face_size-1) -> F3 Left edge
                new_r = faces_config[(1,1)][1] + local_r
                new_c = faces_config[(1,1)][2]
                new_facing = 0 # Right
            elif facing == 1: # Down (local_r=face_size-1) -> F6 Top edge
                new_r = faces_config[(3,0)][1]
                new_c = faces_config[(3,0)][2] + local_c
                new_facing = 1 # Down

        # Face 3: (1, 1) in face_idx coordinates
        elif face_id == 3:
            if facing == 3: # Up (local_r=0) -> F1 Bottom edge
                new_r = faces_config[(0,1)][1] + (face_size - 1)
                new_c = faces_config[(0,1)][2] + local_c
                new_facing = 3 # Up
            elif facing == 2: # Left (local_c=0) -> F2 Right edge
                new_r = faces_config[(1,0)][1] + local_r
                new_c = faces_config[(1,0)][2] + (face_size - 1)
                new_facing = 2 # Left
            elif facing == 0: # Right (local_c=face_size-1) -> F4 Left edge
                new_r = faces_config[(1,2)][1] + local_r
                new_c = faces_config[(1,2)][2]
                new_facing = 0 # Right
            elif facing == 1: # Down (local_r=face_size-1) -> F5 Top edge
                new_r = faces_config[(2,2)][1]
                new_c = faces_config[(2,2)][2] + local_c
                new_facing = 1 # Down

        # Face 4: (1, 2) in face_idx coordinates
        elif face_id == 4:
            if facing == 3: # Up (local_r=0) -> F1 Right edge
                new_r = faces_config[(0,1)][1] + (face_size - 1 - local_c)
                new_c = faces_config[(0,1)][2] + (face_size - 1)
                new_facing = 2 # Left
            elif facing == 2: # Left (local_c=0) -> F3 Right edge
                new_r = faces_config[(1,1)][1] + local_r
                new_c = faces_config[(1,1)][2] + (face_size - 1)
                new_facing = 2 # Left
            elif facing == 0: # Right (local_c=face_size-1) -> F5 Right edge
                new_r = faces_config[(2,2)][1] + (face_size - 1 - local_r)
                new_c = faces_config[(2,2)][2] + (face_size - 1)
                new_facing = 2 # Left
            elif facing == 1: # Down (local_r=face_size-1) -> F5 Left edge
                new_r = faces_config[(2,2)][1] + local_c
                new_c = faces_config[(2,2)][2]
                new_facing = 3 # Up

        # Face 5: (2, 2) in face_idx coordinates
        elif face_id == 5:
            if facing == 3: # Up (local_r=0) -> F3 Bottom edge
                new_r = faces_config[(1,1)][1] + (face_size - 1)
                new_c = faces_config[(1,1)][2] + local_c
                new_facing = 3 # Up
            elif facing == 2: # Left (local_c=0) -> F6 Bottom edge
                new_r = faces_config[(3,0)][1] + (face_size - 1)
                new_c = faces_config[(3,0)][2] + (face_size - 1 - local_r)
                new_facing = 3 # Up
            elif facing == 0: # Right (local_c=face_size-1) -> F4 Right edge
                new_r = faces_config[(1,2)][1] + (face_size - 1 - local_r)
                new_c = faces_config[(1,2)][2] + (face_size - 1)
                new_facing = 2 # Left
            elif facing == 1: # Down (local_r=face_size-1) -> F6 Right edge
                new_r = faces_config[(3,0)][1] + local_c # Corrected
                new_c = faces_config[(3,0)][2] + (face_size - 1)
                new_facing = 2 # Left

        # Face 6: (3, 0) in face_idx coordinates
        elif face_id == 6:
            if facing == 3: # Up (local_r=0) -> F2 Bottom edge
                new_r = faces_config[(1,0)][1] + (face_size - 1)
                new_c = faces_config[(1,0)][2] + local_c
                new_facing = 3 # Up
            elif facing == 2: # Left (local_c=0) -> F1 Top edge
                new_r = faces_config[(0,1)][1]
                new_c = faces_config[(0,1)][2] + local_r
                new_facing = 1 # Down
            elif facing == 0: # Right (local_c=face_size-1) -> F5 Bottom edge
                new_r = faces_config[(2,2)][1] + (face_size - 1)
                new_c = faces_config[(2,2)][2] + local_r
                new_facing = 3 # Up
            elif facing == 1: # Down (local_r=face_size-1) -> F1 Top edge (inverted)
                new_r = faces_config[(0,1)][1]
                new_c = faces_config[(0,1)][2] + (face_size - 1 - local_c)
                new_facing = 1 # Down
        else:
            raise ValueError(f"Real layout: Unhandled cube coordinates for r={r}, c={c}")
    
    return new_r, new_c, new_facing


def solve_part2(input_data):
    # This dictionary holds the face definitions, (face_row_idx, face_col_idx) -> (face_id, global_start_r, global_start_c)
    global faces_config # Make it global to be accessible in get_cube_wrap_coordinates
    faces_config = {}

    board, instructions = parse_input(input_data)

    max_row = len(board)
    max_col_len = max(len(row) for row in board)

    # ic(f"max_row: {max_row}, max_col_len: {max_col_len}")

    grid = []
    for row in board:
        grid.append(list(row) + [' '] * (max_col_len - len(row)))

    face_size = 0
    is_example = False
    
    if max_col_len == 150 and max_row == 200: # Real input size
        face_size = 50
        is_example = False
        faces_config = {
            (0, 1): (1, 0 * face_size, 1 * face_size),         # Face 1
            (0, 2): (2, 0 * face_size, 2 * face_size),         # Face 2
            (1, 1): (3, 1 * face_size, 1 * face_size),         # Face 3
            (2, 0): (4, 2 * face_size, 0 * face_size),         # Face 4
            (2, 1): (5, 2 * face_size, 1 * face_size),         # Face 5
            (3, 0): (6, 3 * face_size, 0 * face_size)          # Face 6
        }
    elif max_col_len == 16 and max_row == 12: # Example input size
        face_size = 4
        is_example = True
        faces_config = {
            (0, 2): (1, 0, 2 * face_size),         # Face 1
            (1, 0): (2, 1 * face_size, 0),         # Face 2
            (1, 1): (3, 1 * face_size, 1 * face_size), # Face 3
            (1, 2): (4, 1 * face_size, 2 * face_size), # Face 4
            (2, 2): (5, 2 * face_size, 2 * face_size), # Face 5
            (2, 3): (6, 2 * face_size, 3 * face_size)  # Face 6
        }
    else:
        raise ValueError(f"Could not infer face size from map dimensions: max_row={max_row}, max_col_len={max_col_len}")

    current_r, current_c = find_start_position(grid)
    facing = 0 # Start facing right

    for num_steps, turn_direction in instructions:
        for _ in range(num_steps):
            next_r, next_c = current_r + dr[facing], current_c + dc[facing]
            next_facing = facing

            is_off_face = False
            # Check if it goes outside the current face's actual boundary (not ' ')
            # Check if next_r, next_c falls into an empty space that is NOT a valid part of another face
            face_id, _, _, _, _ = get_face_info(next_r, next_c, face_size, is_example)
            
            if face_id == -1 or grid[next_r][next_c] == ' ': # If it's not on a valid face, or it's an empty cell
                is_off_face = True
            
            if is_off_face:
                # ic(f"Wrapping: r={current_r}, c={current_c}, facing={facing}")
                next_r, next_c, next_facing = get_cube_wrap_coordinates(current_r, current_c, facing, face_size, is_example)
            
            # Now, next_r, next_c point to a tile on a different face, or wrapped on the same face boundary
            if grid[next_r][next_c] == '#':
                break # Hit a wall, stop moving for this instruction
            elif grid[next_r][next_c] == '.':
                current_r, current_c = next_r, next_c
                facing = next_facing
            # If it's a space, something is wrong with the wrapping logic.

        # Handle turning
        if turn_direction == 'R':
            facing = (facing + 1) % 4
        elif turn_direction == 'L':
            facing = (facing - 1 + 4) % 4
    
    # Password calculation: 1000 * row + 4 * column + facing
    # Rows and columns are 1-indexed
    final_password = 1000 * (current_r + 1) + 4 * (current_c + 1) + facing
    # ic(f"Final position: r={current_r}, c={current_c}, facing={facing}")
    return final_password

def main():
    content = open(0).read()
    result = solve_part2(content) # Use solve_part2 for part 2
    print(result)


if __name__ == "__main__":
    main()