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

    resolved_values = {}

    def get_monkey_value(monkey_name):
        if monkey_name in resolved_values:
            return resolved_values[monkey_name]
        
        job = monkeys[monkey_name]
        
        if isinstance(job, int):
            resolved_values[monkey_name] = job
            return job
        else:
            monkey1_name, operator, monkey2_name = job
            
            val1 = get_monkey_value(monkey1_name)
            val2 = get_monkey_value(monkey2_name)
            
            result = 0
            if operator == '+':
                result = val1 + val2
            elif operator == '-':
                result = val1 - val2
            elif operator == '*':
                result = val1 * val2
            elif operator == '/':
                result = val1 // val2 # Use integer division as per AoC typical patterns
            
            resolved_values[monkey_name] = result
            return result

    return get_monkey_value('root')


def main():
    """Read from stdin and print result."""
    content = open(0).read().strip()
    result = solve(content)
    ic(result)


if __name__ == "__main__":
    main()