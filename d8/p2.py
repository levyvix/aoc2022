from icecream import ic
import math
import sys

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def main():
    content = open(0).read()
    grid = content.splitlines()

    dirs = [(-1, 0), (0, 1), (0, -1), (1, 0)]
    max_trees = -1
    for r, rows in enumerate(grid[1:-1], 1):
        for c, char in enumerate(rows[1:-1], 1):
            current_tree = grid[r][c]
            trees_visible = []
            for d, d2 in dirs:
                i = 0
                s = 0
                hit_boundary = False
                while True:
                    nr = r + (d * (i + 1))
                    nc = c + (d2 * (i + 1))
                    if nr >= len(grid) or nr < 0 or nc >= len(grid[0]) or nc < 0:
                        hit_boundary = True
                        break
                    next_tree = grid[nr][nc]
                    if int(next_tree) < int(current_tree):
                        s += 1
                    else:
                        break
                    i += 1
                if hit_boundary:
                    trees_visible.append(s)
                else:
                    trees_visible.append(s + 1)
            max_trees = max(max_trees, math.prod(trees_visible))
    ic(max_trees)


if __name__ == "__main__":
    main()
