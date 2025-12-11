from icecream import ic
import sys

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def main():
    content = open(0).read()
    grid = content.splitlines()
    edge = len(grid) * 2 + len(grid[0]) * 2 - 4

    dirs = [(-1, 0), (0, 1), (0, -1), (1, 0)]
    visible = 0
    for r, rows in enumerate(grid[1:-1], 1):
        for c, char in enumerate(rows[1:-1], 1):
            current_tree = grid[r][c]
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
                if hit_boundary and i == s:
                    visible += 1
                    break
    ic(visible + edge)


if __name__ == "__main__":
    main()
