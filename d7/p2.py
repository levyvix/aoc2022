from icecream import ic
import sys

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


class Dir:
    def __init__(self, name):
        self.name = name
        self.files = {}
        self.dirs = {}
        self.parent = None

    def size(self):
        total = sum(self.files.values())
        total += sum(d.size() for d in self.dirs.values())
        return total


def main():
    content = open(0).read().strip()

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

    def get_all_sizes(d):
        sizes = [d.size()]
        for child in d.dirs.values():
            sizes.extend(get_all_sizes(child))
        return sizes

    total_size = root.size()
    disk_capacity = 70000000
    free_space = disk_capacity - total_size
    needed_space = 30000000 - free_space

    all_sizes = get_all_sizes(root)
    candidates = [s for s in all_sizes if s >= needed_space]
    result = min(candidates)

    ic(result)


if __name__ == "__main__":
    main()
