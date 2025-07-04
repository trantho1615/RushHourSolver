import heapq
from vehicle import State  # import State from vehicle.py

def heuristic(state):
    red = state.vehicles['X']
    x_end = red.x + red.length
    y = red.y
    return sum(1 for x in range(x_end, state.size) if state.grid[y][x] != '.')

def a_star_solver(start_state):
    frontier = []
    heapq.heappush(frontier, (heuristic(start_state), 0, [start_state], start_state))
    visited = set()

    while frontier:
        f, g, path, current = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)

        if current.is_goal():
            return {
                'solution': path,
                'visited': len(visited),
                'steps': len(path) - 1,
                'cost': g
            }

        for next_state, move_cost in current.get_moves():
            if next_state not in visited:
                new_g = g + move_cost
                new_f = new_g + heuristic(next_state)
                heapq.heappush(frontier, (new_f, new_g, path + [next_state], next_state))

    return None
