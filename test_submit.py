#!/usr/bin/env python3
import requests
import os

day = 25
part = 1
answer = "2-10==12-122-=1-1-22"
session_id = os.environ.get("AOC_SESSION")

response = requests.post(
    f"https://adventofcode.com/2022/day/{day}/answer",
    cookies={"session": session_id},
    data={"level": part, "answer": answer},
)

print(f"Status code: {response.status_code}")
print(f"Response length: {len(response.text)}")

# Look for the main error/success message
if "That's the right answer" in response.text:
    print("✅ CORRECT!")
elif "too high" in response.text:
    print("❌ Answer is too high")
elif "too low" in response.text:
    print("❌ Answer is too low")
elif "not the right answer" in response.text:
    print("❌ Not the right answer")
else:
    print("❌ Some other response")

# Extract the feedback message
import re
match = re.search(r"<p>(.*?either)</p>", response.text, re.DOTALL)
if match:
    feedback = re.sub(r"<[^>]+>", "", match.group(1)).strip()
    print(f"Feedback: {feedback[:300]}")
