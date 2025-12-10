#!/usr/bin/env python3
import requests
import os
import subprocess
import sys

if len(sys.argv) != 3:
    print("Usage: submit.py <day> <part>")
    sys.exit(1)

day = int(sys.argv[1])
part = int(sys.argv[2])

session_id = os.environ.get('AOC_SESSION')
if not session_id:
    print("Error: AOC_SESSION environment variable not set")
    sys.exit(1)

# Run the appropriate Python script to get the answer
script = f"d{day}/p{part}.py"
input_file = f"d{day}/r.in"

try:
    with open(input_file, 'r') as f:
        result = subprocess.run(['uv', 'run', script], stdin=f, capture_output=True, text=True, env=os.environ.copy())
        if result.returncode != 0:
            print(f"Error running {script}:")
            print(f"  stdout: {result.stdout}")
            print(f"  stderr: {result.stderr}")
            sys.exit(1)

    output = result.stdout.strip()
    if not output:
        output = result.stderr.strip()

    if not output:
        print(f"Error: No output from {script}")
        sys.exit(1)

    # Extract the answer from the output (may contain ANSI codes)
    import re

    # Strip ANSI escape codes
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    clean_output = ansi_escape.sub('', output)

    # Look for "result: <number>" or "ans: <number>" pattern
    match = re.search(r'(?:result|ans):\s*(\d+)', clean_output)
    if match:
        answer = match.group(1)
    else:
        # If no pattern match, take the largest number in the output
        numbers = re.findall(r'\d+', clean_output)
        if numbers:
            # Take the longest number (most digits = likely the answer)
            answer = max(numbers, key=len)
        else:
            # If still no match, print the raw output for debugging
            print(f"Error: Could not extract answer from output")
            print(f"Clean output: {repr(clean_output)}")
            sys.exit(1)

    response = requests.post(
        f"https://adventofcode.com/2022/day/{day}/answer",
        cookies={"session": session_id},
        data={"level": part, "answer": answer}
    )

    if "That's the right answer" in response.text:
        print(f"✅ Part {part} correct! Answer: {answer}")
    elif "already complete it" in response.text:
        print(f"✅ Part {part} already completed! Answer: {answer}")
    elif "too high" in response.text:
        print(f"❌ Part {part} too high: {answer}")
    elif "too low" in response.text:
        print(f"❌ Part {part} too low: {answer}")
    else:
        print(f"⚠️  Unexpected response for Part {part}: {answer}")
        print(response.text[:200])
except FileNotFoundError as e:
    print(f"Error: {e}")
    sys.exit(1)
