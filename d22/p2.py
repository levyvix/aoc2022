import numpy as np
import numpy.linalg as lin
import sys

DIRS = [(1, 0, "y", 1), (0, 1, "x", 1), (-1, 0, "y", -1), (0, -1, "x", -1)]

ROTX = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
ROTY = lin.inv(np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]]))
ROT = {"x": ROTX, "y": ROTY}


class Face:
    def __init__(self, tiles=[[]], corners=[], topleft="", coord=()):
        self.tiles: list[list[str]] = tiles
        self.corners: list[str] = corners
        self.topleft: str = topleft
        self.coord: tuple[int, int] = coord


class Cube:
    def __init__(self, terrain):
        self.terrain = terrain
        scale = self.scale()
        self.corners = {
            "a": np.array([-1, -1, -1]),
            "b": np.array([-1, +1, -1]),
            "c": np.array([+1, +1, -1]),
            "d": np.array([+1, -1, -1]),
            "e": np.array([-1, -1, +1]),
            "f": np.array([-1, +1, +1]),
            "g": np.array([+1, +1, +1]),
            "h": np.array([+1, -1, +1]),
        }
        self.faces: list[Face] = []

        bfx = terrain[0].index(".") // scale

        queue: list[tuple[int, int, list]] = [(bfx, 0, [])]
        visited = []

        while queue:
            rx, ry, steps = queue.pop()
            if (rx, ry) in visited:
                continue
            visited.append((rx, ry))
            tmp_face = self.sub_matrix(
                (rx * scale, (rx + 1) * scale - 1), (ry * scale, (ry + 1) * scale - 1)
            )
            for s in steps:
                ax, ax_num = s
                self.rotate(ax, ax_num)
            tmp_tl, tmp_corners = self.front_corners()
            self.faces.append(
                Face(
                    tmp_face,
                    sorted(tmp_corners.keys()),
                    tmp_tl,
                    [rx * scale, ry * scale],
                )
            )
            for dx, dy, ax, ax_num in DIRS:
                try:
                    if (
                        (rx + dx >= 0)
                        and (ry + dy >= 0)
                        and self.terrain[(ry + dy) * scale][(rx + dx) * scale] != " "
                    ):
                        tmp_steps = steps.copy()
                        tmp_steps.append((ax, ax_num))
                        queue.append((rx + dx, ry + dy, tmp_steps))
                except IndexError:
                    pass
            for s in range(len(steps) - 1, -1, -1):
                ax, ax_num = steps[s]
                self.rotate(ax, -ax_num)

    def sub_matrix(self, range1, range2):
        r10, r11 = range1
        r20, r21 = range2
        res = [list(self.terrain[r][r10 : (r11 + 1)]) for r in range(r20, r21 + 1)]
        return np.array(res)

    def scale(self):
        num = sum(1 for row in self.terrain for el in row if el != " ")
        return int((num / 6) ** (1 / 2))

    def front_corners(self):
        corners = {k: v for k, v in self.corners.items() if v[2] == -1}
        tl = [k for k, v in corners.items() if (v[0] == -1) and (v[1] == -1)][0]
        return tl, corners

    def front_face(self):
        _, tmp_corners = self.front_corners()
        tmp_dots = sorted(tmp_corners.keys())
        tmp_face = Face()
        for f in self.faces:
            if f.corners == tmp_dots:
                tmp_face = f
                break
        tmp_tl_pos = tmp_corners[tmp_face.topleft]
        match (tmp_tl_pos[0], tmp_tl_pos[1]):
            case (-1, -1):
                return 0, tmp_face.tiles, tmp_face
            case (-1, 1):
                return 1, np.rot90(tmp_face.tiles), tmp_face
            case (1, 1):
                return 2, np.rot90(tmp_face.tiles, 2), tmp_face
            case _:
                return 3, np.rot90(tmp_face.tiles, 3), tmp_face

    def rotate(self, dim="x", count=1):
        for k, v in self.corners.items():
            self.corners[k] = v @ lin.matrix_power(ROT[dim], count % 4)


def read_data(lines):
    terrain = []
    prog = []
    done = False
    for line in lines:
        line = line.rstrip()
        if line == "":
            done = True
        elif not done:
            terrain.append(line)
        else:
            import re
            tmp = ""
            for i in range(len(line)):
                match line[i]:
                    case "R" | "L":
                        if tmp:
                            prog.append(int(tmp))
                        prog.append(line[i])
                        tmp = ""
                    case _:
                        tmp += line[i]
            if tmp:
                prog.append(int(tmp))
    return terrain, prog


def restore_state(
    pos: tuple[int, int], dir: int, rotates: int, visible: list[list[str]], face: Face
) -> tuple[tuple[int, int], int]:
    x, y = pos
    scale = len(visible[0])
    match rotates:
        case 1:
            x, y = scale - y - 1, x
        case 2:
            x, y = scale - x - 1, scale - y - 1
        case 3:
            x, y = y, scale - x - 1
        case _:
            pass
    dir = (dir + rotates) % 4
    bx, by = face.coord
    return (bx + x, by + y), dir


def step(pos, dir, visible, cube):
    scale = len(visible[0])
    x, y = pos
    dx, dy, ax, ax_num = DIRS[dir]
    nx, ny = x + dx, y + dy
    if (0 <= nx < scale) and (0 <= ny < scale):
        if visible[ny][nx] != "#":
            return (nx, ny), False
    else:
        cube.rotate(ax, ax_num)
        _, tmp_vis, _ = cube.front_face()
        nnx = nx % scale
        nny = ny % scale
        if tmp_vis[nny][nnx] != "#":
            return (nnx, nny), True
        cube.rotate(ax, -ax_num)
    return (x, y), False


def process(prog, cube):
    dir = 0
    cur_rotates, cur_visible, cur_face = cube.front_face()
    x, y = list(cur_visible[0]).index("."), 0
    for c in prog:
        match c:
            case "L":
                dir = (dir - 1) % 4
            case "R":
                dir = (dir + 1) % 4
            case _:
                for _ in range(c):
                    tmp_pos, update = step((x, y), dir, cur_visible, cube)
                    if update:
                        cur_rotates, cur_visible, cur_face = cube.front_face()
                    if (not update) and (tmp_pos == (x, y)):
                        break
                    x, y = tmp_pos
    (x, y), dir = restore_state((x, y), dir, cur_rotates, cur_visible, cur_face)
    score = 1000 * (y + 1) + 4 * (x + 1) + dir
    return (x, y), dir, score


lines = sys.stdin.readlines()
terr, prog = read_data(lines)
cube1 = Cube(terr)
res_pos, res_dir, res_score = process(prog, cube1)
print(res_score)
