from icecream import ic
import sys

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def solve(input_data):
    """Parse input and solve the puzzle."""
    lines = input_data.strip().split('\n')
    
    monkeys = {}
    for line in lines:
        parts = line.split(': ')
        name = parts[0]
        job = parts[1]
        
        if job.isdigit():
            monkeys[name] = int(job)
        else:
            monkeys[name] = job.split(' ')

    # --- Part 1 logic (adapted for Part 2) ---
    # We need to determine which side of 'root' depends on 'humn'
    # and what the other side evaluates to.

    # Function to check if a monkey's value depends on 'humn'
    def depends_on_humn(monkey_name, path=None):
        if path is None:
            path = set()
        if monkey_name == 'humn':
            return True
        
        if monkey_name in path: # Avoid infinite recursion for cycles (though none expected here)
            return False
        path.add(monkey_name)

        job = monkeys[monkey_name]
        if isinstance(job, int):
            return False
        else:
            monkey1_name, _, monkey2_name = job
            return depends_on_humn(monkey1_name, path.copy()) or depends_on_humn(monkey2_name, path.copy())

    # Modified evaluation function for Part 2
    # It takes humn_val as an argument; if humn_val is None, it means we can't
    # evaluate 'humn' numerically, and any path depending on it will raise an error.
    # This allows us to identify the 'humn'-dependent branch.
    resolved_values = {} # Cache for a specific humn_val

    def get_value_for_humn_test(monkey_name, humn_val):
        # Reset cache if humn_val changes, or for initial call
        # For this specific problem, we'll only call with two modes:
        # 1. humn_val = None (to find which branch depends on humn)
        # 2. humn_val = specific number (to evaluate everything)

        if monkey_name == 'humn':
            if humn_val is not None:
                return humn_val
            else:
                # This is the humn monkey and we don't have a value for it yet
                # We raise an exception to signal that this branch depends on humn
                raise ValueError(f"Cannot resolve 'humn' numerically without a value.")
        
        # If we have a value for this monkey from a previous calculation with the same humn_val
        # we can reuse it. This cache is specific to the current 'humn_val' context.
        # This implementation requires clearing or careful handling of resolved_values
        # if get_value_for_humn_test is called multiple times with different humn_val.
        # For this problem, we'll use a local cache within this function scope for clarity,
        # or rely on the iterative nature of the solution where we only need to "evaluate"
        # once for the target, and then "backtrack".

        # For the backtracking, we don't need this resolved_values cache, as we are
        # going in reverse. For forward evaluation, we could use a global resolved_values
        # but need to clear it or scope it per `humn_val`.
        # Let's just recompute for now for simplicity, as the graph is not extremely deep.

        job = monkeys[monkey_name]
        
        if isinstance(job, int):
            return job
        else:
            monkey1_name, operator, monkey2_name = job
            
            val1 = get_value_for_humn_test(monkey1_name, humn_val)
            val2 = get_value_for_humn_test(monkey2_name, humn_val)
            
            if operator == '+':
                return val1 + val2
            elif operator == '-':
                return val1 - val2
            elif operator == '*':
                return val1 * val2
            elif operator == '/':
                return val1 // val2
            else:
                raise ValueError(f"Unknown operator: {operator}")


    # Identify root's children
    root_job = monkeys['root']
    root_left_child, _, root_right_child = root_job

    # Determine which child depends on 'humn'
    left_depends = depends_on_humn(root_left_child)
    right_depends = depends_on_humn(root_right_child)

    humn_dependent_child = None
    known_value_child = None
    target_value = None

    if left_depends:
        humn_dependent_child = root_left_child
        known_value_child = root_right_child
        # Evaluate the known side (right child)
        target_value = get_value_for_humn_test(known_value_child, None) # humn_val is None, but this branch shouldn't hit 'humn'
    elif right_depends:
        humn_dependent_child = root_right_child
        known_value_child = root_left_child
        # Evaluate the known side (left child)
        target_value = get_value_for_humn_test(known_value_child, None) # humn_val is None, but this branch shouldn't hit 'humn'
    else:
        raise RuntimeError("Neither root child depends on humn, or both do (unexpected).")

    # Now, backtrack from humn_dependent_child to find the value of 'humn'
    def find_humn_input(current_monkey, required_output):
        if current_monkey == 'humn':
            return required_output
        
        job = monkeys[current_monkey]
        monkey1_name, operator, monkey2_name = job

        # Determine which child is on the humn path and which is known
        child1_depends = depends_on_humn(monkey1_name)
        child2_depends = depends_on_humn(monkey2_name)

        if child1_depends and child2_depends:
            raise RuntimeError("Both children depend on humn, unsupported for this method.")
        
        if child1_depends:
            # child1 is the unknown, child2 is known
            known_val = get_value_for_humn_test(monkey2_name, None)
            
            if operator == '+':
                needed_val_for_child1 = required_output - known_val
            elif operator == '-':
                needed_val_for_child1 = required_output + known_val # required_output = child1 - known_val => child1 = required_output + known_val
            elif operator == '*':
                needed_val_for_child1 = required_output // known_val
            elif operator == '/':
                needed_val_for_child1 = required_output * known_val # required_output = child1 / known_val => child1 = required_output * known_val
            else:
                raise ValueError(f"Unknown operator: {operator}")
            
            return find_humn_input(monkey1_name, needed_val_for_child1)
        
        elif child2_depends:
            # child2 is the unknown, child1 is known
            known_val = get_value_for_humn_test(monkey1_name, None)

            if operator == '+':
                needed_val_for_child2 = required_output - known_val
            elif operator == '-':
                needed_val_for_child2 = known_val - required_output # required_output = known_val - child2 => child2 = known_val - required_output
            elif operator == '*':
                needed_val_for_child2 = required_output // known_val
            elif operator == '/':
                needed_val_for_child2 = known_val // required_output # required_output = known_val / child2 => child2 = known_val / required_output
            else:
                raise ValueError(f"Unknown operator: {operator}")
            
            return find_humn_input(monkey2_name, needed_val_for_child2)
        else:
            raise RuntimeError(f"Neither child of {current_monkey} depends on humn, but expected one to.")

    return find_humn_input(humn_dependent_child, target_value)


def main():
    """Read from stdin and print result."""
    content = open(0).read().strip()
    result = solve(content)
    ic(result)


if __name__ == "__main__":
    main()
