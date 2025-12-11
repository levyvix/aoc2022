from icecream import ic
import sys
import re

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def parse_blueprints(input_data):
    """Parse blueprint definitions."""
    blueprints = []
    text = input_data.strip()

    # Join lines between blueprints to handle multi-line format
    text = re.sub(r'\n  Each', ' Each', text)

    for line in text.split('\n'):
        if not line.strip() or not line.startswith('Blueprint'):
            continue

        match = re.match(r'Blueprint (\d+):', line)
        if match:
            bp_id = int(match.group(1))

            ore_robot = int(re.search(r'ore robot costs (\d+) ore', line).group(1))
            clay_robot = int(re.search(r'clay robot costs (\d+) ore', line).group(1))
            obsidian_robot_ore = int(re.search(r'obsidian robot costs (\d+) ore', line).group(1))
            obsidian_robot_clay = int(re.search(r'obsidian robot costs \d+ ore and (\d+) clay', line).group(1))
            geode_robot_ore = int(re.search(r'geode robot costs (\d+) ore', line).group(1))
            geode_robot_obsidian = int(re.search(r'geode robot costs \d+ ore and (\d+) obsidian', line).group(1))

            blueprints.append({
                'id': bp_id,
                'ore': ore_robot,
                'clay': clay_robot,
                'obsidian': (obsidian_robot_ore, obsidian_robot_clay),
                'geode': (geode_robot_ore, geode_robot_obsidian)
            })
    return blueprints


def max_geodes(blueprint, time_limit=32):
    """Find maximum geodes using DFS with memoization and strategic pruning."""
    max_ore_needed = max(blueprint['ore'],
                        blueprint['clay'],
                        blueprint['obsidian'][0],
                        blueprint['geode'][0])
    max_clay_needed = blueprint['obsidian'][1]

    # Memoization cache
    memo = {}
    best = [0]

    def dfs(minutes_left, ore, clay, obsidian, geodes,
            ore_robots, clay_robots, obsidian_robots, geode_robots):
        """DFS with memoization and aggressive pruning."""

        # Base cases
        if minutes_left == 0:
            best[0] = max(best[0], geodes)
            return geodes

        if minutes_left == 1:
            # Only collect one more round of resources
            return geodes + geode_robots

        # Memoization key
        state = (minutes_left, ore, clay, obsidian,
                 ore_robots, clay_robots, obsidian_robots, geode_robots)
        if state in memo:
            return memo[state]

        # Upper bound pruning: theoretical max if we built geode robot every remaining minute
        theoretical_max = geodes + (geode_robots * minutes_left) + ((minutes_left * (minutes_left - 1)) // 2)
        if theoretical_max <= best[0]:
            memo[state] = 0
            return 0

        max_result = 0

        # Priority 1: Build geode robot if possible (greedy geode strategy)
        if ore >= blueprint['geode'][0] and obsidian >= blueprint['geode'][1]:
            new_ore = ore - blueprint['geode'][0] + ore_robots
            new_obsidian = obsidian - blueprint['geode'][1] + obsidian_robots
            result = dfs(minutes_left - 1, new_ore, clay + clay_robots, new_obsidian,
                        geodes + geode_robots, ore_robots, clay_robots, obsidian_robots, geode_robots + 1)
            max_result = max(max_result, result)
        else:
            # Build other robots strategically

            # Try building obsidian robot if needed
            if (ore >= blueprint['obsidian'][0] and clay >= blueprint['obsidian'][1] and
                obsidian_robots < blueprint['geode'][1]):
                new_ore = ore - blueprint['obsidian'][0] + ore_robots
                new_clay = clay - blueprint['obsidian'][1] + clay_robots
                result = dfs(minutes_left - 1, new_ore, new_clay, obsidian + obsidian_robots,
                            geodes + geode_robots, ore_robots, clay_robots, obsidian_robots + 1, geode_robots)
                max_result = max(max_result, result)

            # Try building clay robot if needed
            if ore >= blueprint['clay'] and clay_robots < max_clay_needed:
                new_ore = ore - blueprint['clay'] + ore_robots
                result = dfs(minutes_left - 1, new_ore, clay + clay_robots, obsidian + obsidian_robots,
                            geodes + geode_robots, ore_robots, clay_robots + 1, obsidian_robots, geode_robots)
                max_result = max(max_result, result)

            # Try building ore robot if needed
            if ore >= blueprint['ore'] and ore_robots < max_ore_needed:
                new_ore = ore - blueprint['ore'] + ore_robots
                result = dfs(minutes_left - 1, new_ore, clay + clay_robots, obsidian + obsidian_robots,
                            geodes + geode_robots, ore_robots + 1, clay_robots, obsidian_robots, geode_robots)
                max_result = max(max_result, result)

            # Try waiting (collect resources)
            result = dfs(minutes_left - 1, ore + ore_robots, clay + clay_robots, obsidian + obsidian_robots,
                        geodes + geode_robots, ore_robots, clay_robots, obsidian_robots, geode_robots)
            max_result = max(max_result, result)

        best[0] = max(best[0], max_result)
        memo[state] = max_result
        return max_result

    dfs(time_limit, 0, 0, 0, 0, 1, 0, 0, 0)

    return best[0]


def solve(input_data):
    """Parse input and solve the puzzle."""
    blueprints = parse_blueprints(input_data)

    # Part 2 uses only the first 3 blueprints with 32 minute time limit
    result = 1
    for bp in blueprints[:3]:
        geodes = max_geodes(bp, time_limit=32)
        ic(f"Blueprint {bp['id']}: {geodes} geodes")
        result *= geodes

    return result


def main():
    """Read from stdin and print result."""
    content = open(0).read()
    result = solve(content)
    print(result)


if __name__ == "__main__":
    main()
