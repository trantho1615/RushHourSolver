from collections import deque
import heapq


def bfs(initilia_state, max_depth=25):
    """
    Find solutions to given Problem board using breadth first search.
    Returns a dictionary with named fields:
        visited: the number of configurations visited in the search
        solutions: paths to the goal state
        depth_states: the number of states visited at each depth

    Arguments:
        r: A Problem board.

    Keyword Arguments:
        max_depth: Maximum depth to traverse in search (default=25)
    """
    visited = set()
    solutions = list()
    depth_states = dict()

    queue = deque()
    queue.appendleft((initilia_state, tuple()))
    while len(queue) != 0:
        board, path = queue.pop()
        new_path = path + tuple([board])

        depth_states[len(new_path)] = depth_states.get(len(new_path), 0) + 1

        if len(new_path) >= max_depth:
            break

        if board in visited:
            continue
        else:
            visited.add(board)

        if board.solved():
            solutions.append(new_path)
        else:
            queue.extendleft((move, new_path) for move in board.moves())

    return {'visited': visited,
            'solutions': solutions,
            'depth_states': depth_states}


def ucs(initial_state):
    """
    Find solutions to the given problem board using Uniform Cost Search.
    Returns a dictionary with named fields:
        visited: the set of configurations visited in the search
        solutions: a list of paths to the goal state
    """
    visited = set()
    solutions = list()

    # Priority queue stores tuples of (cost, path, board)
    priority_queue = [(0, [initial_state], initial_state)]

    while priority_queue:
        cost, path, board = heapq.heappop(priority_queue)

        if board in visited:
            continue

        visited.add(board)

        if board.solved():
            solutions.append(path)
            # Since we want to find all solutions, we continue searching
            # If we only wanted the optimal solution, we could break here
            continue

        for move in board.moves():
            if move not in visited:
                moved_vehicle = list(board.vehicles - move.vehicles)[0]
                new_cost = cost + moved_vehicle.length
                new_path = path + [move]
                heapq.heappush(priority_queue, (new_cost, new_path, move))

    return {'visited': visited, 'solutions': solutions}