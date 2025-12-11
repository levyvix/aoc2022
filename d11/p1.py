def parse_monkeys(input_data):
    """Parse monkey data from input."""
    monkeys = []
    blocks = input_data.strip().split("\n\n")

    for block in blocks:
        lines = block.strip().split("\n")

        # Parse starting items
        items_line = lines[1].split(": ")[1]
        items = list(map(int, items_line.split(", ")))

        # Parse operation
        op_line = lines[2].split("= ")[1]

        # Parse test divisor
        test_div = int(lines[3].split("by ")[1])

        # Parse throw targets
        true_target = int(lines[4].split("monkey ")[1])
        false_target = int(lines[5].split("monkey ")[1])

        monkeys.append(
            {
                "items": items,
                "operation": op_line,
                "test_div": test_div,
                "true_target": true_target,
                "false_target": false_target,
                "inspections": 0,
            }
        )

    return monkeys


def apply_operation(old, op_str):
    """Apply operation string to old value."""
    # op_str is like "old * 19" or "old + 6" or "old * old"
    parts = op_str.split()
    operand1 = old if parts[0] == "old" else int(parts[0])
    operator = parts[1]
    operand2 = old if parts[2] == "old" else int(parts[2])

    if operator == "+":
        return operand1 + operand2
    elif operator == "*":
        return operand1 * operand2
    else:
        raise ValueError(f"Unknown operator: {operator}")


def simulate_round(monkeys):
    """Simulate one round of monkey business."""
    for monkey in monkeys:
        while monkey["items"]:
            # Inspect item
            item = monkey["items"].pop(0)
            monkey["inspections"] += 1

            # Apply operation
            worry = apply_operation(item, monkey["operation"])

            # Monkey gets bored (divide by 3 and round down)
            worry //= 3

            # Test and throw
            if worry % monkey["test_div"] == 0:
                monkeys[monkey["true_target"]]["items"].append(worry)
            else:
                monkeys[monkey["false_target"]]["items"].append(worry)


def solve(input_data):
    """Parse input and solve the puzzle."""
    monkeys = parse_monkeys(input_data)

    # Simulate 20 rounds
    for _ in range(20):
        simulate_round(monkeys)

    # Get the two most active monkeys
    inspections = sorted([m["inspections"] for m in monkeys], reverse=True)
    result = inspections[0] * inspections[1]

    return result


def main():
    """Read from stdin and print result."""
    content = open(0).read().strip()
    result = solve(content)
    print(result)


if __name__ == "__main__":
    main()
