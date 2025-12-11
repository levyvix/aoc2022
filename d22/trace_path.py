# Manual trace of example path
# Grid (0-indexed):
#     01234567890123456
#  0      ...#
#  1      .#..
#  2      #...
#  3      ....
#  4  ...#.......#
#  5  ........#...
#  6  ..#....#....
#  7  ..........#.
#  8      ...#....
#  9      .....#..
# 10      .#......
# 11      ......#.

# Path: 10R5L5R10L4R5L5
# Start: row 0, col 8 (first '.' in face 1), facing RIGHT (0)

print("Expected final: row 5, col 7, facing 3")
print("Which is row 4, col 6 in 0-indexed, facing UP")
print()
print("Face 3 spans rows 4-7, cols 4-7")
print("So final position is in Face 3, local coords (0, 2)")
