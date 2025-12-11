# AoC 2022 Day 22 Part 2: Cube Wrapping Solution

## Understanding the Problem

The example input has this net (4×4 faces):
```
        1111
        1111        Face 1: rows 0-3, cols 8-11
        1111
        1111
222233334444        Face 2: rows 4-7, cols 0-3
222233334444        Face 3: rows 4-7, cols 4-7
222233334444        Face 4: rows 4-7, cols 8-11
222233334444
        55556666    Face 5: rows 8-11, cols 8-11
        55556666    Face 6: rows 8-11, cols 12-15
        55556666
        55556666
```

## How to Visualize the Cube

The standard way to fold this net is:
- **Face 1** = TOP
- **Face 2** = LEFT (when viewed from front)
- **Face 3** = FRONT
- **Face 4** = RIGHT (when viewed from front)
- **Face 5** = BOTTOM
- **Face 6** = BACK

Imagine folding:
1. Face 3 stays as the "front" base
2. Face 1 folds up to become the top
3. Face 2 folds to the left
4. Face 4 folds to the right
5. Face 5 folds down to become the bottom
6. Face 6 wraps around to the back

## Key Insight: Edge Pairings

On a cube, each edge touches exactly one other edge. When you walk off an edge in the 2D net, you need to figure out:
1. Which face you're entering
2. Which edge of that face you're entering from
3. Your new facing direction
4. Whether the coordinates are reversed along the edge

## Working Out Transitions for Example

Let me work through each face and its 4 edges:

### Face 1 (TOP) - rows 0-3, cols 8-11

1. **Going UP (facing=3) from top edge (row 0)**
   - In 3D: top of TOP face connects to... it wraps to face 2
   - Actually, let me think about this more carefully by folding
   - Face 2's top edge (row 4) touches Face 1's top edge (row 0), but REVERSED
   - When you exit F1 going up at (0, col), you enter F2 at (4, 3-(col-8))
   - New facing: DOWN (1) because you flipped over the edge

2. **Going LEFT (facing=2) from left edge (col 8)**
   - F1's left edge connects to F3's top edge when folded
   - Exit F1 at (row, 8) → enter F3 at (4, 4+row)
   - New facing: DOWN (1)

3. **Going RIGHT (facing=0) from right edge (col 11)**
   - F1's right edge connects to F6's top edge (reversed) when folded
   - Exit F1 at (row, 11) → enter F6 at (8, 15-row)
   - New facing: DOWN (1)

4. **Going DOWN (facing=1) from bottom edge (row 3)**
   - This is a natural connection in the net: F1 bottom → F4 top
   - Exit F1 at (3, col) → enter F4 at (4, col)
   - New facing: DOWN (1)

### Face 2 (LEFT) - rows 4-7, cols 0-3

1. **Going UP (facing=3) from top edge (row 4)**
   - Connects to F1 top edge (reversed)
   - Exit F2 at (4, col) → enter F1 at (0, 11-(col-0))
   - New facing: DOWN (1)

2. **Going LEFT (facing=2) from left edge (col 0)**
   - Wraps around cube to F6's bottom edge (reversed)
   - Exit F2 at (row, 0) → enter F6 at (11, 15-(row-4))
   - New facing: UP (3)

3. **Going RIGHT (facing=0) from right edge (col 3)**
   - Natural connection: F2 right → F3 left
   - Exit F2 at (row, 3) → enter F3 at (row, 4)
   - New facing: RIGHT (0)

4. **Going DOWN (facing=1) from bottom edge (row 7)**
   - Wraps to F5 bottom edge (reversed)
   - Exit F2 at (7, col) → enter F5 at (11, 11-(col-0))
   - New facing: UP (3)

### Face 3 (FRONT) - rows 4-7, cols 4-7

1. **Going UP (facing=3) from top edge (row 4)**
   - Connects to F1 left edge
   - Exit F3 at (4, col) → enter F1 at (col-4, 8)
   - New facing: RIGHT (0)

2. **Going LEFT (facing=2) from left edge (col 4)**
   - Natural connection: F3 left → F2 right
   - Exit F3 at (row, 4) → enter F2 at (row, 3)
   - New facing: LEFT (2)

3. **Going RIGHT (facing=0) from right edge (col 7)**
   - Natural connection: F3 right → F4 left
   - Exit F3 at (row, 7) → enter F4 at (row, 8)
   - New facing: RIGHT (0)

4. **Going DOWN (facing=1) from bottom edge (row 7)**
   - Connects to F5 left edge (reversed)
   - Exit F3 at (7, col) → enter F5 at (11-(col-4), 8)
   - New facing: RIGHT (0)

### Face 4 (RIGHT) - rows 4-7, cols 8-11

1. **Going UP (facing=3) from top edge (row 4)**
   - Natural connection: F4 top → F1 bottom
   - Exit F4 at (4, col) → enter F1 at (3, col)
   - New facing: UP (3)

2. **Going LEFT (facing=2) from left edge (col 8)**
   - Natural connection: F4 left → F3 right
   - Exit F4 at (row, 8) → enter F3 at (row, 7)
   - New facing: LEFT (2)

3. **Going RIGHT (facing=0) from right edge (col 11)**
   - Wraps to F6 right edge (reversed)
   - Exit F4 at (row, 11) → enter F6 at (11-(row-4), 15)
   - New facing: LEFT (2)

4. **Going DOWN (facing=1) from bottom edge (row 7)**
   - Natural connection: F4 bottom → F5 top
   - Exit F4 at (7, col) → enter F5 at (8, col)
   - New facing: DOWN (1)

### Face 5 (BOTTOM) - rows 8-11, cols 8-11

1. **Going UP (facing=3) from top edge (row 8)**
   - Natural connection: F5 top → F4 bottom
   - Exit F5 at (8, col) → enter F4 at (7, col)
   - New facing: UP (3)

2. **Going LEFT (facing=2) from left edge (col 8)**
   - Connects to F3 bottom edge (reversed)
   - Exit F5 at (row, 8) → enter F3 at (7, 7-(row-8))
   - New facing: UP (3)

3. **Going RIGHT (facing=0) from right edge (col 11)**
   - Natural connection: F5 right → F6 left
   - Exit F5 at (row, 11) → enter F6 at (row, 12)
   - New facing: RIGHT (0)

4. **Going DOWN (facing=1) from bottom edge (row 11)**
   - Wraps to F2 bottom edge (reversed)
   - Exit F5 at (11, col) → enter F2 at (7, 3-(col-8))
   - New facing: UP (3)

### Face 6 (BACK) - rows 8-11, cols 12-15

1. **Going UP (facing=3) from top edge (row 8)**
   - Connects to F1 right edge (reversed)
   - Exit F6 at (8, col) → enter F1 at (3-(col-12), 11)
   - New facing: LEFT (2)

2. **Going LEFT (facing=2) from left edge (col 12)**
   - Natural connection: F6 left → F5 right
   - Exit F6 at (row, 12) → enter F5 at (row, 11)
   - New facing: LEFT (2)

3. **Going RIGHT (facing=0) from right edge (col 15)**
   - Wraps to F4 right edge (reversed)
   - Exit F6 at (row, 15) → enter F4 at (7-(row-8), 11)
   - New facing: LEFT (2)

4. **Going DOWN (facing=1) from bottom edge (row 11)**
   - Wraps to F2 left edge (reversed)
   - Exit F6 at (11, col) → enter F2 at (7-(col-12), 0)
   - New facing: RIGHT (0)

## Algorithm

1. For each (face_id, exit_direction) pair, pre-compute:
   - Target face_id
   - Entry direction on target face
   - Whether the edge position is reversed
   - Formula to convert (local_row, local_col) to new coordinates

2. When moving:
   - Calculate next position
   - If it's off the current face (or into ' '), use the transition map
   - Check if new position is a wall

## Common Mistakes

1. **Forgetting to reverse coordinates** on certain edges
2. **Wrong facing direction** after transition
3. **Confusing entry vs exit directions** - when you exit RIGHT, you enter from the LEFT on the new face
