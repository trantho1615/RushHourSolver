from collections import deque

from collections import deque

def bfs(initial_state, max_depth=100):
    """
    Breadth-First Search solver for the Rush Hour puzzle.

    Args:
        initial_state (Problem): The initial board configuration.
        max_depth (int): Maximum search depth to prevent infinite loops.

    Returns:
        dict: {
            'visited': Set of visited states,
            'solutions': List of solution paths (each is a tuple of Problem states),
            'depth_states': Dict of {depth: number of states at that depth}
        }
    """
    visited = set()
    solutions = []
    depth_states = {}

    # queue holds tuples of (current_state, path_to_state)
    queue = deque()
    queue.appendleft((initial_state, tuple()))

    while queue:
        current, path = queue.pop()
        new_path = path + (current,)

        depth = len(new_path)
        depth_states[depth] = depth_states.get(depth, 0) + 1

        # Limit search depth to avoid infinite loops in complex unsolvable boards
        if depth > max_depth:
            continue

        if current in visited:
            continue
        visited.add(current)

        if current.solved():
            solutions.append(new_path)
            continue  # Optional: break here if you only want one solution

        for move in current.moves():
            queue.appendleft((move, new_path))

    return {
        'visited': visited,
        'solutions': solutions,
        'depth_states': depth_states
    }