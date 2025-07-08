from collections import deque
import heapq

"""python main.py Map/p1 a*"""
def bfs(initilia_state, max_depth=100):
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


#Depth First Search (DFS) algorithm
def dfs(initial_state):
    #Initializes
    visited = set()
    solutions = list()
    depth_states = dict()
    #Stack to keep track to current path
    stack = []
    stack.append((initial_state, tuple()))
    while len(stack) != 0:
        board, path = stack.pop()
        new_path = path + tuple([board])
        depth_states[len(new_path)] = depth_states.get(len(new_path), 0) + 1

        if board in visited:
            continue
        else:
            visited.add(board)

        if board.solved():
            solutions.append(new_path)
        else:
            stack.extend((move, new_path) for move in board.moves())

    # Return all found solutions
    return {'visited': visited,
            'solutions': solutions,
            'depth_states': depth_states}

def dls(initial_state, limit=100):
    visited = dict()       #Must use dict to track depth
    solutions = []
    depth_states = dict()

    stack = []
    stack.append((initial_state, tuple()))  # (state, path)

    while stack:
        board, path = stack.pop()
        new_path = path + (board,)
        depth = len(new_path)

        depth_states[depth] = depth_states.get(depth, 0) + 1

        if board in visited and visited[board] <= depth:
            continue
        visited[board] = depth

        if board.solved():
            solutions.append(new_path)
        elif depth < limit:
            for move in board.moves():
                stack.append((move, new_path))

    # Return all found solutions within the limit
    return {
        'solutions': solutions,
        'depth_states': depth_states,
        'visited': visited
    }