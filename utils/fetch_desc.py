#!/usr/bin/env python3
"""Fetch Advent of Code problem descriptions."""

import os
import sys
import re
import html
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: uv add requests", file=sys.stderr)
    sys.exit(1)


def fetch_descriptions(day: int) -> tuple[str, str]:
    """Fetch part 1 and part 2 descriptions from AOC."""
    session_id = os.getenv("AOC_SESSION")
    if not session_id:
        print("Error: AOC_SESSION environment variable not set", file=sys.stderr)
        sys.exit(1)

    url = f"https://adventofcode.com/2022/day/{day}"
    cookies = {"session": session_id}

    try:
        response = requests.get(url, cookies=cookies, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        sys.exit(1)

    content = response.text

    # Find all article elements (day-desc articles can have optional id attribute)
    article_pattern = r'<article[^>]*class="day-desc"[^>]*>(.*?)</article>'
    articles = re.findall(article_pattern, content, re.DOTALL)

    if not articles:
        return "", ""

    # First article is part 1, second is part 2 (if it exists)
    part1 = clean_html(articles[0]) if articles else ""
    part2 = clean_html(articles[1]) if len(articles) > 1 else ""

    return part1, part2


def clean_html(html_text: str) -> str:
    """Convert HTML to plain text."""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', html_text)

    # Decode HTML entities
    text = html.unescape(text)

    # Fix spacing
    # Remove lines that are just whitespace
    lines = [line.rstrip() for line in text.split('\n')]
    lines = [line for line in lines if line.strip()]

    # Join with newlines, preserving structure
    text = '\n'.join(lines)

    return text.strip()


def main():
    if len(sys.argv) < 2:
        print("Usage: fetch_desc.py <day> [output_dir]", file=sys.stderr)
        sys.exit(1)

    try:
        day = int(sys.argv[1])
    except ValueError:
        print(f"Error: Invalid day '{sys.argv[1]}'", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(f"d{day}")
    output_dir.mkdir(exist_ok=True)

    part1, part2 = fetch_descriptions(day)

    # Write files
    desc1_file = output_dir / "desc1.txt"
    desc2_file = output_dir / "desc2.txt"

    desc1_file.write_text(part1 + "\n" if part1 else "")
    desc2_file.write_text(part2 + "\n" if part2 else "")

    print(f"Saved to {desc1_file} and {desc2_file}")


if __name__ == "__main__":
    main()
