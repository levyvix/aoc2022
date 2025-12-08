# Advent of Code 2022

Solutions for [Advent of Code 2022](https://adventofcode.com/2022) - a series of daily programming puzzles.

## Setup

### Prerequisites

- Python 3.12+
- [UV package manager](https://docs.astral.sh/uv/)

### Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   uv sync
   ```

3. Set up your Advent of Code session token in `.envrc`:
   - Go to [adventofcode.com](https://adventofcode.com)
   - Open browser developer tools (DevTools)
   - Find the `session` cookie value
   - Add to `.envrc`:
     ```bash
     export AOC_SESSION=your_session_token_here
     ```
   - Run `direnv allow` to load the environment

## Usage

### Create a new day

```bash
just md [day_number]
```

Or create today's puzzle:
```bash
just md
```

This will:
- Create a new directory (`d1/`, `d2/`, etc.)
- Generate `p1.py` boilerplate file.
- Download the puzzle input (`r.in`) and test example (`t.in`)

### Solve a puzzle

Edit `d[number]/p1.py` and `d[number]/p2.py` with your solutions. Use `ic()` from the icecream library to print results:

```python
from icecream import ic

def solve(input_data):
    # Your solution here
    return result

ic(solve(open('r.in').read()))
```

### Run a solution

```bash
uv run d1/p1.py
uv run d2/p2.py
```

## Project Structure

```
aoc2022/
├── d1/                 # Day 1 solutions
│   ├── p1.py         # Part 1 solution
│   ├── p2.py         # Part 2 solution
│   ├── r.in          # Real puzzle input
│   └── t.in          # Test/example input
├── d2/ - d6/          # Additional days
├── utils/             # Utility functions
│   ├── __init__.py
│   └── make_day.py   # Script to scaffold new days
├── justfile           # Task automation
├── pyproject.toml     # Project configuration
├── .envrc             # Environment variables (direnv)
└── uv.lock            # Dependency lock file
```

## Progress

## Dependencies

- **advent-of-code-data** - Automatically fetches puzzle inputs and examples
- **icecream** - Pretty debugging output

## Tips

- Use `t.in` to test with provided examples before running with real input (`r.in`)
- Each part's solution goes in its own file (`p1.py`, `p2.py`)
- The `make_day.py` utility creates consistent boilerplate for each day
