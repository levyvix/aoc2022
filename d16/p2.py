from icecream import ic
import sys
from collections import defaultdict, deque

ic.configureOutput(outputFunction=lambda s: print(s, file=sys.stderr))


def solve(input_data):
    """Parse input and solve the puzzle."""
    lines = input_data.strip().split('\n')

    # Parse input
    graph = defaultdict(list)
    flow_rates = {}

    for line in lines:
        parts = line.split('; ')
        valve_part = parts[0].split()
        valve = valve_part[1]
        flow = int(valve_part[4].split('=')[1])

        tunnels_part = parts[1]
        if 'tunnels' in tunnels_part:
            tunnel_list = tunnels_part.replace('tunnels lead to valves ', '').split(', ')
        else:
            tunnel_list = tunnels_part.replace('tunnel leads to valve ', '').split(', ')

        graph[valve] = tunnel_list
        flow_rates[valve] = flow

    # Find all non-zero flow valves
    important_valves = sorted([v for v in flow_rates if flow_rates[v] > 0])

    # Precompute shortest paths using BFS
    dist_cache = {}

    def shortest_path(start, end):
        if (start, end) in dist_cache:
            return dist_cache[(start, end)]
        if start == end:
            return 0
        queue = deque([(start, 0)])
        visited = {start}
        while queue:
            node, d = queue.popleft()
            if node == end:
                dist_cache[(start, end)] = d
                return d
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, d + 1))
        dist_cache[(start, end)] = float('inf')
        return float('inf')

    # Convert important_valves list to frozenset for set operations
    all_important = frozenset(important_valves)

    # Memoization for single agent (given a subset of available valves)
    memo_single = {}

    def best_pressure_single_agent(available_valves):
        """Best pressure for one agent with access to available_valves (26 minutes)."""
        available_key = frozenset(available_valves)
        if available_key in memo_single:
            return memo_single[available_key]

        memo = {}

        def dfs_single(current, time_remaining, opened):
            if time_remaining <= 0:
                return 0

            key = (current, time_remaining, opened)
            if key in memo:
                return memo[key]

            best = 0

            # Try opening each unopened valve in available set
            for valve in available_valves:
                if valve not in opened:
                    dist = shortest_path(current, valve)
                    time_to_open = dist + 1

                    if time_to_open < time_remaining:
                        new_time = time_remaining - time_to_open
                        pressure = flow_rates[valve] * new_time
                        new_opened = opened | frozenset([valve])
                        future = dfs_single(valve, new_time, new_opened)
                        best = max(best, pressure + future)

            memo[key] = best
            return best

        result = dfs_single('AA', 26, frozenset())
        memo_single[available_key] = result
        return result

    # For each possible partition of valves, calculate total pressure
    # But use lazy evaluation - only try partitions where valves are split reasonably
    max_pressure = 0

    # Collect all reachable valve subsets by doing a single DFS
    reachable_subsets = set()

    def collect_subsets(current, time_remaining, opened):
        """Collect all reachable opened valve sets."""
        opened_frozen = frozenset(opened)
        if opened_frozen in reachable_subsets:
            return
        reachable_subsets.add(opened_frozen)

        for valve in important_valves:
            if valve not in opened:
                dist = shortest_path(current, valve)
                time_to_open = dist + 1

                if time_to_open < time_remaining:
                    new_time = time_remaining - time_to_open
                    new_opened = opened | {valve}
                    collect_subsets(valve, new_time, new_opened)

    # Collect all reachable subsets
    collect_subsets('AA', 26, set())

    # For each reachable subset, pair it with its complement and find best
    for subset in reachable_subsets:
        complement = all_important - subset
        pressure_1 = best_pressure_single_agent(subset)
        pressure_2 = best_pressure_single_agent(complement)
        max_pressure = max(max_pressure, pressure_1 + pressure_2)

    return max_pressure


def main():
    """Read from stdin and print result."""
    content = open(0).read().strip()
    result = solve(content)
    ic(result)


if __name__ == "__main__":
    main()
