#!/usr/bin/env python3
import requests
import os
import subprocess
import sys

if len(sys.argv) < 3 or len(sys.argv) > 4:
    print("Usage: submit.py <day> <part> [answer]")
    sys.exit(1)

day = int(sys.argv[1])
part = int(sys.argv[2])
answer = sys.argv[3] if len(sys.argv) == 4 else None

session_id = os.environ.get("AOC_SESSION")
if not session_id:
    print("Error: AOC_SESSION environment variable not set")
    sys.exit(1)

# If no answer provided, run the script to get it
if not answer:
    script = f"d{day}/p{part}.py"
    input_file = f"d{day}/r.in"

    try:
        with open(input_file, "r") as f:
            # Day 22 part 2 requires numpy
            cmd = ["uv", "run", script]
            if day == 22 and part == 2:
                cmd = ["uv", "run", "--with", "numpy", script]

            result = subprocess.run(
                cmd,
                stdin=f,
                capture_output=True,
                text=True,
                env=os.environ.copy(),
            )
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
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        clean_output = ansi_escape.sub("", output)

        # Look for "result: <number>" or "ans: <number>" pattern (handles both numbers and SNAFU)
        match = re.search(r"(?:result|ans):\s*([\w\-=]+)", clean_output)
        if match:
            answer = match.group(1)
        else:
            # If no pattern match, try to extract the answer
            # First try to get SNAFU-like answers for day 25 (contains -, =, and digits)
            if day == 25 and part == 1:
                snafu_match = re.search(r"[\d\-=2]+", clean_output.strip())
                if snafu_match:
                    answer = snafu_match.group(0).strip()
                else:
                    print("Error: Could not extract SNAFU answer from output")
                    print(f"Clean output: {repr(clean_output)}")
                    sys.exit(1)
            else:
                # Fall back to taking the largest number in the output
                numbers = re.findall(r"\d+", clean_output)
                if numbers:
                    # Take the longest number (most digits = likely the answer)
                    answer = max(numbers, key=len)
                else:
                    # For part 2 visual puzzles (like day 10), the answer is usually multi-line text
                    # Try to extract capital letters from the output
                    if part == 2:
                        # Extract sequences of capital letters and common characters
                        lines = clean_output.split("\n")
                        # Join all capital letters and common word characters found in the output
                        all_text = "".join(lines)
                        # Look for capital letter sequences (the OCR answer)
                        letter_match = re.search(r"[A-Z]{4,}", all_text)
                        if letter_match:
                            answer = letter_match.group(0)
                        else:
                            # If no capital letter sequence, use the full output for manual inspection
                            print("Note: Could not auto-extract answer from output")
                            print(f"Full output:\n{clean_output}")
                            print(
                                "\nPlease visually identify the 8 capital letters and submit manually"
                            )
                            sys.exit(1)
                    else:
                        # If still no match for part 1, print the raw output for debugging
                        print("Error: Could not extract answer from output")
                        print(f"Clean output: {repr(clean_output)}")
                        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

response = requests.post(
    f"https://adventofcode.com/2022/day/{day}/answer",
    cookies={"session": session_id},
    data={"level": part, "answer": answer},
)

# Look for various success indicators in the response
if "That's the right answer" in response.text:
    print(f"✅ Part {part} correct! Answer: {answer}")
elif "already complete it" in response.text or "You don't" in response.text:
    print(f"✅ Part {part} already completed! Answer: {answer}")
elif "too high" in response.text:
    print(f"❌ Part {part} too high: {answer}")
elif "too low" in response.text:
    print(f"❌ Part {part} too low: {answer}")
elif (
    "not the right answer" in response.text
    or "right answer" not in response.text.lower()
):
    # If we get the full HTML page back without a success message, likely wrong answer
    print(f"❌ Part {part} incorrect: {answer}")
    # Try to extract the feedback message
    import re

    match = re.search(r"<p>(.*?either)</p>", response.text, re.DOTALL)
    if match:
        feedback = re.sub(r"<[^>]+>", "", match.group(1)).strip()
        print(f"   Feedback: {feedback[:200]}")
else:
    print(f"⚠️  Ambiguous response for Part {part}: {answer}")
    # For text answers, this might actually be correct - let's assume it is
    print("   (Submitting text answer - please verify on AoC website)")
