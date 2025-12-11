# AoC 2022 Day 22 Part 2: Cube Wrapping Explanation

## Problem Summary

You're given a 2D net of a cube and need to follow a path with proper 3D cube wrapping.

## Key Concepts

### 1. Understanding Cube Folding

When a 2D net folds into a 3D cube, edges that are separate in the net become adjacent in 3D. The challenge is determining:
- **Which face** you transition to
- **Which edge** of that face you enter from  
- **Your new facing direction**
- **Whether coordinates are reversed** along the edge

### 2. Clean Algorithm for Cube Wrapping

Rather than hardcoding every transition, you can:

**Step 1: Define face layout**
Map out which (face_row, face_col) grid positions correspond to which face IDs and their global coordinates.

**Step 2: Build transition table**
For each (face_id, exit_direction) pair, define:
- Target face ID
- Entry edge on target face
- Whether the edge mapping is reversed
- Transformation formula for coordinates

**Step 3: Apply transitions**
When moving off a face:
1. Detect you're leaving the current face
2. Look up the transition in your table
3. Calculate new global coordinates from local coordinates
4. Update position and facing

### 3. Coordinate Systems

Work with three coordinate systems:
- **Global**: Absolute position in the 2D grid (row, col)
- **Face**: Which face you're on (face_row_idx, face_col_idx)
- **Local**: Position within the face (local_row, local_col)

Convert between them to handle transitions cleanly.

## Common Pitfalls

1. **Off-by-one errors**: Carefully track 0-indexed vs 1-indexed coordinates
2. **Forgetting to reverse**: Many edges connect in reversed order
3. **Wrong facing**: When you exit RIGHT, you typically enter from LEFT on the new face, but with cube wrapping this isn't always true
4. **Premature wrapping**: Make sure you detect wrapping at the right time (when the NEXT position would be off the face, not when you're already off)

## For This Specific Problem

The example input uses 4×4 faces arranged as:
```
    1111
    1111
    1111
    1111
222233334444
222233334444
222233334444
222233334444
    55556666
    55556666
    55556666
    55556666
```

Expected final answer: **5031** (row 5, col 7, facing UP in 1-indexed coordinates)

## Sources

- [Advent of Code 2022 - Day 22 (Todd Ginsberg)](https://todd.ginsberg.com/post/advent-of-code/2022/day22/)
- [Advent of Code 2022 Day 22 - DEV Community](https://dev.to/nickymeuleman/advent-of-code-2022-day-22-4m2)
- [Day 22 Solutions Megathread (Reddit)](https://www.reddit.com/r/adventofcode/comments/zsct8w/2022_day_22_solutions/)

