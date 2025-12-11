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
    valve_to_idx = {v: i for i, v in enumerate(important_valves)}

    # Precompute shortest paths using BFS
    def shortest_path(start, end):
        if start == end:
            return 0
        queue = deque([(start, 0)])
        visited = {start}
        while queue:
            node, dist = queue.popleft()
            if node == end:
                return dist
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        return float('inf')

    memo = {}

    def dfs(current, time_remaining, opened_mask):
        if time_remaining <= 0:
            return 0

        key = (current, time_remaining, opened_mask)
        if key in memo:
            return memo[key]

        best = 0

        # Try opening each unopened valve
        for i, valve in enumerate(important_valves):
            if not (opened_mask & (1 << i)):  # If valve not open
                dist = shortest_path(current, valve)
                time_to_open = dist + 1
                if time_to_open < time_remaining:  # Must have time to benefit
                    new_time = time_remaining - time_to_open
                    pressure = flow_rates[valve] * new_time
                    new_opened = opened_mask | (1 << i)
                    future = dfs(valve, new_time, new_opened)
                    best = max(best, pressure + future)

        memo[key] = best
        return best

    result = dfs('AA', 30, 0)
    return result


def main():
    """Read from stdin and print result."""
    content = open(0).read().strip()
    result = solve(content)
    ic(result)


if __name__ == "__main__":
    main()
