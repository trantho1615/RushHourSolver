from collections import deque
import heapq

def heuristic(state):
    """
    Heuristic function for A*:
    Returns the number of vehicles blocking the red car ('X') from reaching the exit.
    """
    board = state.get_board()
    for v in state.vehicles:
        if v.id == 'X':
            red = v
            break
    else:
        return float('inf')  # X not found

    count = 0
    y = red.y
    x_end = red.x + red.length
    for x in range(x_end, 6):  # Check cells to the right of red car
        if board[y][x] != ' ':
            count += 1
    return count


def a_star_solver(initial_state):
    """
    A* search for solving the Rush Hour puzzle.
    Returns a dictionary with:
        'visited': set of visited states
        'solutions': list of solution paths
        'depth_states': dict mapping depth -> number of states
    """

    visited = set()
    solutions = []
    depth_states = dict()

    # Priority queue: (f = g + h, g = cost, path, current_state)
    queue = []
    heapq.heappush(queue, (heuristic(initial_state), 0, [initial_state], initial_state))

    while queue:
        f, g, path, board = heapq.heappop(queue)
        depth = len(path)
        depth_states[depth] = depth_states.get(depth, 0) + 1

        if board in visited:
            continue
        visited.add(board)

        if board.solved():
            solutions.append(path)
            return {
                'visited': visited,
                'solutions': solutions,
                'depth_states': depth_states
            }

        for move in board.moves():
            if move not in visited:
                # Find which vehicle moved to compute cost
                moved_vehicle = list(board.vehicles - move.vehicles)[0]
                move_cost = moved_vehicle.length
                new_g = g + move_cost
                new_f = new_g + heuristic(move)
                heapq.heappush(queue, (new_f, new_g, path + [move], move))

    return {
        'visited': visited,
        'solutions': [],
        'depth_states': depth_states
    }