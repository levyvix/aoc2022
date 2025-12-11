# Cube Net Analysis for AoC 2022 Day 22 Part 2

## Example Net Layout (4x4 faces)
```
    1111        Face 1: rows 0-3, cols 8-11
    1111
    1111
    1111
222233334444    Face 2: rows 4-7, cols 0-3
222233334444    Face 3: rows 4-7, cols 4-7
222233334444    Face 4: rows 4-7, cols 8-11
222233334444
    55556666    Face 5: rows 8-11, cols 8-11
    55556666    Face 6: rows 8-11, cols 12-15
    55556666
    55556666
```

## 3D Cube Visualization

If we fold this net into a cube where:
- Face 1 = TOP
- Face 2 = LEFT
- Face 3 = FRONT
- Face 4 = RIGHT
- Face 5 = BOTTOM
- Face 6 = BACK

## Edge Connections (14 transitions total)

### Face 1 (Top) - 4 edges
1. **F1 Top → F2 Top** (reversed)
   - F1 going UP (facing=3) at row 0 → F2 at row 4, FACING DOWN (1)
   - Position mapping: F1[0, col] → F2[4, 3-col]

2. **F1 Left → F3 Top**
   - F1 going LEFT (facing=2) at col 8 → F3 at row 4, FACING DOWN (1)
   - Position mapping: F1[row, 8] → F3[4, 4+row]

3. **F1 Right → F6 Top** (reversed)
   - F1 going RIGHT (facing=0) at col 11 → F6 at row 8, FACING DOWN (1)
   - Position mapping: F1[row, 11] → F6[8, 15-row]

4. **F1 Bottom → F4 Top**
   - F1 going DOWN (facing=1) at row 3 → F4 at row 4, FACING DOWN (1)
   - Position mapping: F1[3, col] → F4[4, col]

### Face 2 (Left) - 4 edges
5. **F2 Top → F1 Top** (reversed) [reverse of #1]
   - F2 going UP (facing=3) at row 4 → F1 at row 0, FACING DOWN (1)
   - Position mapping: F2[4, col] → F1[0, 11-col]

6. **F2 Left → F6 Bottom** (reversed)
   - F2 going LEFT (facing=2) at col 0 → F6 at row 11, FACING UP (3)
   - Position mapping: F2[row, 0] → F6[11, 15-(row-4)]

7. **F2 Right → F3 Left**
   - F2 going RIGHT (facing=0) at col 3 → F3 at col 4, FACING RIGHT (0)
   - Position mapping: F2[row, 3] → F3[row, 4]

8. **F2 Bottom → F5 Bottom** (reversed)
   - F2 going DOWN (facing=1) at row 7 → F5 at row 11, FACING UP (3)
   - Position mapping: F2[7, col] → F5[11, 11-(col)]

### Face 3 (Front) - 4 edges
9. **F3 Top → F1 Left** [reverse of #2]
   - F3 going UP (facing=3) at row 4 → F1 at col 8, FACING RIGHT (0)
   - Position mapping: F3[4, col] → F1[col-4, 8]

10. **F3 Left → F2 Right** [reverse of #7]
    - F3 going LEFT (facing=2) at col 4 → F2 at col 3, FACING LEFT (2)
    - Position mapping: F3[row, 4] → F2[row, 3]

11. **F3 Right → F4 Left**
    - F3 going RIGHT (facing=0) at col 7 → F4 at col 8, FACING RIGHT (0)
    - Position mapping: F3[row, 7] → F4[row, 8]

12. **F3 Bottom → F5 Left** (reversed)
    - F3 going DOWN (facing=1) at row 7 → F5 at col 8, FACING RIGHT (0)
    - Position mapping: F3[7, col] → F5[11-(col-4), 8]

### Face 4 (Right) - 4 edges
13. **F4 Top → F1 Bottom** [reverse of #4]
    - F4 going UP (facing=3) at row 4 → F1 at row 3, FACING UP (3)
    - Position mapping: F4[4, col] → F1[3, col]

14. **F4 Left → F3 Right** [reverse of #11]
    - F4 going LEFT (facing=2) at col 8 → F3 at col 7, FACING LEFT (2)
    - Position mapping: F4[row, 8] → F3[row, 7]

15. **F4 Right → F6 Right** (reversed)
    - F4 going RIGHT (facing=0) at col 11 → F6 at col 15, FACING LEFT (2)
    - Position mapping: F4[row, 11] → F6[11-(row-4), 15]

16. **F4 Bottom → F5 Top**
    - F4 going DOWN (facing=1) at row 7 → F5 at row 8, FACING DOWN (1)
    - Position mapping: F4[7, col] → F5[8, col]

### Face 5 (Bottom) - 4 edges
17. **F5 Top → F4 Bottom** [reverse of #16]
    - F5 going UP (facing=3) at row 8 → F4 at row 7, FACING UP (3)
    - Position mapping: F5[8, col] → F4[7, col]

18. **F5 Left → F3 Bottom** (reversed) [reverse of #12]
    - F5 going LEFT (facing=2) at col 8 → F3 at row 7, FACING UP (3)
    - Position mapping: F5[row, 8] → F3[7, 11-(row-8)]

19. **F5 Right → F6 Left**
    - F5 going RIGHT (facing=0) at col 11 → F6 at col 12, FACING RIGHT (0)
    - Position mapping: F5[row, 11] → F6[row, 12]

20. **F5 Bottom → F2 Bottom** (reversed) [reverse of #8]
    - F5 going DOWN (facing=1) at row 11 → F2 at row 7, FACING UP (3)
    - Position mapping: F5[11, col] → F2[7, 11-(col-8)]

### Face 6 (Back) - 4 edges
21. **F6 Top → F1 Right** (reversed) [reverse of #3]
    - F6 going UP (facing=3) at row 8 → F1 at col 11, FACING LEFT (2)
    - Position mapping: F6[8, col] → F1[15-(col-12), 11]

22. **F6 Left → F5 Right** [reverse of #19]
    - F6 going LEFT (facing=2) at col 12 → F5 at col 11, FACING LEFT (2)
    - Position mapping: F6[row, 12] → F5[row, 11]

23. **F6 Right → F4 Right** (reversed) [reverse of #15]
    - F6 going RIGHT (facing=0) at col 15 → F4 at col 11, FACING LEFT (2)
    - Position mapping: F6[row, 15] → F4[11-(row-8), 11]

24. **F6 Bottom → F2 Left** (reversed) [reverse of #6]
    - F6 going DOWN (facing=1) at row 11 → F2 at col 0, FACING RIGHT (0)
    - Position mapping: F6[11, col] → F2[11-(col-12), 0]

## Testing the Expected Answer

Expected final position: row 5, col 7, facing 3 (UP)
- This is row 5, col 7 in 1-indexed coords
- In 0-indexed: row 4, col 6
- Face: Face 3 (rows 4-7, cols 4-7)
- Local coords: (0, 2) within Face 3

The path is: 10R5L5R10L4R5L5

Let's trace this manually to verify the transitions are correct.
