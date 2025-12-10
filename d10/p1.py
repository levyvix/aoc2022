from icecream import ic
import sys

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def solve(input_data):
    """Parse input and solve the puzzle."""
    lines = input_data.strip().split('\n')

    x = 1
    cycle = 0
    signal_strengths = []
    target_cycles = {20, 60, 100, 140, 180, 220}

    for line in lines:
        if line == 'noop':
            cycle += 1
            if cycle in target_cycles:
                signal_strengths.append(cycle * x)
        else:  # addx V
            v = int(line.split()[1])
            # First cycle of addx
            cycle += 1
            if cycle in target_cycles:
                signal_strengths.append(cycle * x)
            # Second cycle of addx
            cycle += 1
            if cycle in target_cycles:
                signal_strengths.append(cycle * x)
            # After second cycle, update x
            x += v

    result = sum(signal_strengths)
    return result


def main():
    """Read from stdin and print result."""
    content = open(0).read().strip()
    result = solve(content)
    ic(result)


if __name__ == "__main__":
    main()
