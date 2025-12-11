from icecream import ic
import sys

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))

DEC_KEY = 811589153


def solve(input_data):
    """Parse input and solve the puzzle."""
    numbers = [int(line) for line in input_data.strip().split('\n')]
    
    # Apply decryption key
    numbers = [num * DEC_KEY for num in numbers]

    # Store (original_index, value) pairs to maintain original order for mixing
    # This list will be modified during mixing
    mixed_list = [(i, num) for i, num in enumerate(numbers)]
    
    list_len = len(numbers)

    # Perform mixing 10 times
    for _ in range(10): # Loop 10 times for mixing
        for i in range(list_len):
            # Find the current position of the element with original_index i
            current_idx = -1
            for j, (original_idx, value) in enumerate(mixed_list):
                if original_idx == i:
                    current_idx = j
                    break
            
            # Remove the element from its current position
            element_to_move = mixed_list.pop(current_idx)
            
            # Calculate the new position
            if element_to_move[1] == 0:
                new_idx = current_idx
            else:
                # The list length decreases by 1 after pop, so modulo by list_len - 1
                # Python's % operator handles negative numbers for circular wrapping
                new_idx = (current_idx + element_to_move[1]) % (list_len - 1)
            
            # Insert the element at the new position
            mixed_list.insert(new_idx, element_to_move)

    # Find the index of the number 0 in the final mixed list
    zero_idx = -1
    for i, (original_idx, value) in enumerate(mixed_list):
        if value == 0:
            zero_idx = i
            break
            
    # Calculate grove coordinates
    # Wrap around the list using modulo list_len
    coord1_val = mixed_list[(zero_idx + 1000) % list_len][1]
    coord2_val = mixed_list[(zero_idx + 2000) % list_len][1]
    coord3_val = mixed_list[(zero_idx + 3000) % list_len][1]
    
    return coord1_val + coord2_val + coord3_val


def main():
    """Read from stdin and print result."""
    content = open(0).read().strip()
    result = solve(content)
    ic(result)


if __name__ == "__main__":
    main()
