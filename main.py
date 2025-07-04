from vehicle import Vehicle, State
from solver import a_star_solver

def create_sample_map():
    return [
        Vehicle('X', 1, 2, 2, 'H'),  # Red car
        Vehicle('A', 0, 0, 2, 'V'),
        Vehicle('B', 3, 0, 3, 'V'),
        Vehicle('C', 5, 0, 3, 'V'),
        Vehicle('D', 0, 3, 3, 'H'),
        Vehicle('E', 4, 3, 2, 'V'),
        Vehicle('F', 2, 5, 3, 'H'),
    ]

def print_state(state, step=None):
    if step is not None:
        print(f"Step {step}")
    for row in state.grid:
        print(' '.join(row))
    print("--------")

if __name__ == "__main__":
    vehicles = create_sample_map()
    start_state = State(vehicles)

    result = a_star_solver(start_state)

    if result:
        print(f"Steps: {result['steps']}")
        print(f"Total cost: {result['cost']}")
        print(f"Visited nodes: {result['visited']}")
        print("\nSolution path:\n")
        for idx, state in enumerate(result['solution']):
            print_state(state, idx)
    else:
        print("No solution found.")
