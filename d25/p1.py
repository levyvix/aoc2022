
def snafu_to_decimal(snafu):
    """Convert a SNAFU number to decimal."""
    digits = {
        '2': 2,
        '1': 1,
        '0': 0,
        '-': -1,
        '=': -2,
    }

    result = 0
    power = 0

    # Process digits from right to left
    for char in reversed(snafu):
        result += digits[char] * (5 ** power)
        power += 1

    return result


def decimal_to_snafu(decimal):
    """Convert a decimal number to SNAFU."""
    if decimal == 0:
        return '0'

    digits = ['0', '1', '2', '=', '-']
    result = []

    while decimal > 0:
        remainder = decimal % 5
        decimal //= 5

        # Map remainder to SNAFU digit
        # 0 -> 0, 1 -> 1, 2 -> 2, 3 -> =, 4 -> -
        if remainder <= 2:
            result.append(digits[remainder])
        else:
            # For 3 and 4, we need to "borrow" from the next position
            result.append(digits[remainder])
            decimal += 1

    return ''.join(reversed(result))


def solve(input_data):
    """Parse input and solve the puzzle."""
    lines = input_data.strip().split('\n')

    # Convert all SNAFU numbers to decimal and sum
    total = 0
    for snafu in lines:
        if snafu.strip():
            decimal = snafu_to_decimal(snafu.strip())
            total += decimal

    # Convert the total back to SNAFU
    result = decimal_to_snafu(total)

    return result


def main():
    """Read from stdin and print result."""
    content = open(0).read().strip()
    result = solve(content)
    print(result)


if __name__ == "__main__":
    main()
