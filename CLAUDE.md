# Advent of Code 2022 - Development Workflow

## Quick Reference

```bash
# Create a new day
just md 9

# Fetch problem descriptions
just desc 9

# Test solutions
cd d9 && just t1    # Test part 1
cd d9 && just t2    # Test part 2

# Run with real input
cd d9 && just r1    # Run part 1
cd d9 && just r2    # Run part 2

# Submit answers
just submit 1 9     # Submit day 9 part 1
just submit 2 9     # Submit day 9 part 2
```

## Detailed Workflow

### 1. Create a New Day Template

Use the `just md` command to scaffold a new day:

```bash
just md 9
```

This will automatically:
- Create a `d9/` directory
- Generate `p1.py` with boilerplate code
- Generate `p2.py` (empty, ready for part 2)
- Download the real puzzle input to `r.in`
- Download the test/example input to `t.in`
- Create a `justfile` with task shortcuts

**Files created:**
```
d9/
├── p1.py          # Part 1 solution
├── p2.py          # Part 2 solution
├── r.in           # Real puzzle input
├── t.in           # Test/example input
├── justfile       # Local task shortcuts
├── desc1.txt      # Part 1 description (empty until fetched)
└── desc2.txt      # Part 2 description (empty until fetched)
```

### 2. Fetch Problem Descriptions

After solving part 1 and it's accepted, fetch the descriptions:

```bash
just desc 9
```

This will:
- Fetch part 1 description from adventofcode.com and save to `d9/desc1.txt`
- Fetch part 2 description from adventofcode.com and save to `d9/desc2.txt`

**Note:** Part 2 description only becomes available after you submit a correct answer for part 1.

### 3. Solution Template

Each solution should follow this structure:

```python
from icecream import ic
import sys

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def solve(input_data):
    """Parse input and solve the puzzle."""
    lines = input_data.strip().split('\n')

    # Your solution logic here
    result = 0

    return result


def main():
    """Read from stdin and print result."""
    content = open(0).read().strip()
    result = solve(content)
    ic(result)


if __name__ == "__main__":
    main()
```

**Key points:**
- Read from stdin using `open(0).read()`
- Configure icecream to output to stderr so only the answer goes to stdout
- Return just the numeric answer from `solve()`
- Use `ic()` to debug (prints to stderr)

### 4. Testing Solutions

**Test with example input:**

From the day directory:
```bash
cd d9
just t1     # Test part 1
just t2     # Test part 2
```

From the project root:
```bash
uv run d9/p1.py < d9/t.in
uv run d9/p2.py < d9/t.in
```

The test input is small and should run instantly. Compare output to expected result in the problem description.

### 5. Running with Real Input

**Run with the actual puzzle input:**

From the day directory:
```bash
cd d9
just r1     # Run part 1
just r2     # Run part 2
```

From the project root:
```bash
uv run d9/p1.py < d9/r.in
uv run d9/p2.py < d9/r.in
```

### 6. Submitting Solutions

**Submit your answer to Advent of Code:**

From the project root:
```bash
just submit 1 9     # Submit day 9 part 1
just submit 2 9     # Submit day 9 part 2
```

The submit script will:
- Extract the numeric answer from your solution output
- Submit it to adventofcode.com
- Confirm if the answer is correct
- Display any feedback if incorrect

**Requirements:**
- `AOC_SESSION` environment variable must be set with your session cookie
- Your solution must output the answer in one of these formats:
  - `result: <answer>`
  - `ans: <answer>`
  - Or just a number (the largest number found)

### 7. Standard Workflow

1. **Create day:** `just md 9`
2. **Fetch descriptions:** `just desc 9` (after part 1 accepted)
3. **Edit solutions:** Update `d9/p1.py` and `d9/p2.py`
4. **Test part 1:** `cd d9 && just t1`
5. **Run part 1:** `cd d9 && just r1`
6. **Submit part 1:** `just submit 1 9`
7. **Fetch part 2 description:** `just desc 9`
8. **Test part 2:** `cd d9 && just t2`
9. **Run part 2:** `cd d9 && just r2`
10. **Submit part 2:** `just submit 2 9`

## Important Notes

### Debugging with icecream

Use `ic()` to inspect values:
```python
def solve(input_data):
    lines = input_data.strip().split('\n')
    ic(f"Number of lines: {len(lines)}")  # Prints to stderr
    # ... rest of solution
```

The icecream output goes to stderr and won't interfere with the submitted answer.

### Common Issues

**Problem:** `just t1` says "Justfile does not contain recipe `t1`"
- **Solution:** You must be in the `d9/` directory. Run: `cd d9 && just t1`

**Problem:** Solution runs but submit says format is wrong
- **Solution:** Make sure the numeric answer is the last output line. Use icecream for debug output.

**Problem:** Part 2 description is empty
- **Solution:** Submit part 1 first, then run `just desc 9` again to fetch part 2.

## Utility Scripts

- `utils/make_day.py` - Creates day scaffold
- `utils/fetch_desc.py` - Fetches problem descriptions from AoC (with year hardcoded to 2022)
- `utils/submit.py` - Submits answers to AoC

**Note:** When copying `fetch_desc.py` from other AoC projects, ensure the year is set to 2022 in the URL:
```python
url = f"https://adventofcode.com/2022/day/{day}"
```
