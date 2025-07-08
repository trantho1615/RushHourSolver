from collections import deque

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

def dls(initial_state, limit=25):
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