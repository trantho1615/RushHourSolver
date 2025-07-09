import heapq

def heuristic(problem):
    board = problem.get_board()
    for v in problem.vehicles:
        if v.id == 'X':
            x_end = v.x + v.length
            row = v.y
            return sum(1 for x in range(x_end, 6) if board[row][x] != ' ')
    return 0

def a_star(problem):
    visited = set()
    frontier = []
    heapq.heappush(frontier, (heuristic(problem), 0, [problem], problem))

    while frontier:
        f, g, path, current = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)

        if current.solved():
            return {'visited': visited, 'solutions': [path]}

        for next_state in current.moves():
            if next_state not in visited:
                moved = list(current.vehicles - next_state.vehicles)[0]
                cost = moved.length
                heapq.heappush(frontier, (g + cost + heuristic(next_state), g + cost, path + [next_state], next_state))

    return {'visited': visited, 'solutions': []}
