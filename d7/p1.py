from icecream import ic
from pathlib import Path

file_name = "r.in"
content = (Path(__file__).parent / file_name).read_text().strip()

# Build filesystem tree
class Dir:
    def __init__(self, name):
        self.name = name
        self.files = {}  # {name: size}
        self.dirs = {}   # {name: Dir}
        self.parent = None

    def size(self):
        total = sum(self.files.values())
        total += sum(d.size() for d in self.dirs.values())
        return total

root = Dir("/")
current = root

for line in content.split("\n"):
    parts = line.split()

    if parts[0] == "$":
        if parts[1] == "cd":
            dirname = parts[2]
            if dirname == "/":
                current = root
            elif dirname == "..":
                current = current.parent
            else:
                if dirname not in current.dirs:
                    new_dir = Dir(dirname)
                    new_dir.parent = current
                    current.dirs[dirname] = new_dir
                current = current.dirs[dirname]
        elif parts[1] == "ls":
            pass
    else:
        if parts[0] == "dir":
            dirname = parts[1]
            if dirname not in current.dirs:
                new_dir = Dir(dirname)
                new_dir.parent = current
                current.dirs[dirname] = new_dir
        else:
            size = int(parts[0])
            filename = parts[1]
            current.files[filename] = size

# Find all directories and sum those <= 100000
def find_small_dirs(d):
    total = 0
    if d.size() <= 100000:
        total += d.size()
    for child in d.dirs.values():
        total += find_small_dirs(child)
    return total

result = find_small_dirs(root)
ic(result)
