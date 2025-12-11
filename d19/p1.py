import re


def parse_blueprints(input_data):
    """Parse blueprint definitions."""
    blueprints = []
    text = input_data.strip()

    # Join lines between blueprints to handle multi-line format
    text = re.sub(r"\n  Each", " Each", text)

    for line in text.split("\n"):
        if not line.strip() or not line.startswith("Blueprint"):
            continue

        match = re.match(r"Blueprint (\d+):", line)
        if match:
            bp_id = int(match.group(1))

            ore_robot = int(re.search(r"ore robot costs (\d+) ore", line).group(1))
            clay_robot = int(re.search(r"clay robot costs (\d+) ore", line).group(1))
            obsidian_robot_ore = int(
                re.search(r"obsidian robot costs (\d+) ore", line).group(1)
            )
            obsidian_robot_clay = int(
                re.search(r"obsidian robot costs \d+ ore and (\d+) clay", line).group(1)
            )
            geode_robot_ore = int(
                re.search(r"geode robot costs (\d+) ore", line).group(1)
            )
            geode_robot_obsidian = int(
                re.search(r"geode robot costs \d+ ore and (\d+) obsidian", line).group(
                    1
                )
            )

            blueprints.append(
                {
                    "id": bp_id,
                    "ore": ore_robot,
                    "clay": clay_robot,
                    "obsidian": (obsidian_robot_ore, obsidian_robot_clay),
                    "geode": (geode_robot_ore, geode_robot_obsidian),
                }
            )
    return blueprints


def max_geodes(blueprint, time_limit=24):
    """Find maximum geodes obtainable with a blueprint in given time."""
    from collections import deque

    max_ore_needed = max(
        blueprint["ore"],
        blueprint["clay"],
        blueprint["obsidian"][0],
        blueprint["geode"][0],
    )

    best = [0]
    visited = set()

    # BFS with state: (minute, ore, clay, obsidian, ore_robots, clay_robots, obsidian_robots, geode_robots)
    queue = deque([(0, 0, 0, 0, 0, 1, 0, 0, 0)])

    while queue:
        (
            minute,
            ore,
            clay,
            obsidian,
            geodes,
            ore_robots,
            clay_robots,
            obsidian_robots,
            geode_robots,
        ) = queue.popleft()

        if minute == time_limit:
            best[0] = max(best[0], geodes)
            continue

        remaining = time_limit - minute

        # Prune states that can't possibly beat the best result
        # Even if we build geode robots every remaining turn
        theoretical_max = (
            geodes + geode_robots * remaining + (remaining * (remaining - 1)) // 2
        )
        if theoretical_max <= best[0]:
            continue

        state = (
            minute,
            ore,
            clay,
            obsidian,
            ore_robots,
            clay_robots,
            obsidian_robots,
            geode_robots,
        )
        if state in visited:
            continue
        visited.add(state)

        # Try all possible actions
        actions = []

        # Try building geode robot
        if ore >= blueprint["geode"][0] and obsidian >= blueprint["geode"][1]:
            actions.append(
                (
                    ore - blueprint["geode"][0],
                    clay,
                    obsidian - blueprint["geode"][1],
                    ore_robots,
                    clay_robots,
                    obsidian_robots,
                    geode_robots + 1,
                )
            )

        # Try building obsidian robot
        if ore >= blueprint["obsidian"][0] and clay >= blueprint["obsidian"][1]:
            if obsidian_robots < blueprint["geode"][1]:
                actions.append(
                    (
                        ore - blueprint["obsidian"][0],
                        clay - blueprint["obsidian"][1],
                        obsidian,
                        ore_robots,
                        clay_robots,
                        obsidian_robots + 1,
                        geode_robots,
                    )
                )

        # Try building clay robot
        if ore >= blueprint["clay"]:
            if clay_robots < blueprint["obsidian"][1]:
                actions.append(
                    (
                        ore - blueprint["clay"],
                        clay,
                        obsidian,
                        ore_robots,
                        clay_robots + 1,
                        obsidian_robots,
                        geode_robots,
                    )
                )

        # Try building ore robot
        if ore >= blueprint["ore"]:
            if ore_robots < max_ore_needed:
                actions.append(
                    (
                        ore - blueprint["ore"],
                        clay,
                        obsidian,
                        ore_robots + 1,
                        clay_robots,
                        obsidian_robots,
                        geode_robots,
                    )
                )

        # Try waiting (do nothing)
        actions.append(
            (
                ore,
                clay,
                obsidian,
                ore_robots,
                clay_robots,
                obsidian_robots,
                geode_robots,
            )
        )

        # Process all actions
        for (
            new_ore,
            new_clay,
            new_obsidian,
            new_ore_robots,
            new_clay_robots,
            new_obsidian_robots,
            new_geode_robots,
        ) in actions:
            # Collect resources after action
            final_ore = new_ore + ore_robots
            final_clay = new_clay + clay_robots
            final_obsidian = new_obsidian + obsidian_robots
            final_geodes = geodes + geode_robots
            queue.append(
                (
                    minute + 1,
                    final_ore,
                    final_clay,
                    final_obsidian,
                    final_geodes,
                    new_ore_robots,
                    new_clay_robots,
                    new_obsidian_robots,
                    new_geode_robots,
                )
            )

    return best[0]


def solve(input_data):
    """Parse input and solve the puzzle."""
    blueprints = parse_blueprints(input_data)

    quality_sum = 0
    for bp in blueprints:
        geodes = max_geodes(bp)
        quality = bp["id"] * geodes
        print(f"Blueprint {bp['id']}: {geodes} geodes, quality {quality}")
        quality_sum += quality

    return quality_sum


def main():
    """Read from stdin and print result."""
    content = open(0).read()
    result = solve(content)
    print(result)


if __name__ == "__main__":
    main()
