from vehicle import Vehicle

GOAL_VEHICLE = Vehicle('X', 4, 2, 'H')

class Problem:

    def __init__(self, vehicles):
        self.vehicles = vehicles  # set of Vehicle objects

    def __hash__(self):
        return hash(tuple(sorted(self.vehicles)))

    def __eq__(self, other):
        return self.vehicles == other.vehicles

    def __lt__(self, other):
        return hash(self) < hash(other)

    def get_board(self):
        board = [[' ' for _ in range(6)] for _ in range(6)]
        for v in self.vehicles:
            if v.orientation == 'H':
                for i in range(v.length):
                    board[v.y][v.x + i] = v.id
            else:
                for i in range(v.length):
                    board[v.y + i][v.x] = v.id
        return board

    def solved(self):
        return GOAL_VEHICLE in self.vehicles

    def moves(self):
        board = self.get_board()
        for v in sorted(self.vehicles):
            if v.orientation == 'H':
                # Move left
                if v.x - 1 >= 0 and board[v.y][v.x - 1] == ' ':
                    new_v = Vehicle(v.id, v.x - 1, v.y, v.orientation)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    yield Problem(new_vehicles)
                # Move right
                if v.x + v.length < 6 and board[v.y][v.x + v.length] == ' ':
                    new_v = Vehicle(v.id, v.x + 1, v.y, v.orientation)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    yield Problem(new_vehicles)
            else:
                # Move up
                if v.y - 1 >= 0 and board[v.y - 1][v.x] == ' ':
                    new_v = Vehicle(v.id, v.x, v.y - 1, v.orientation)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    yield Problem(new_vehicles)
                # Move down
                if v.y + v.length < 6 and board[v.y + v.length][v.x] == ' ':
                    new_v = Vehicle(v.id, v.x, v.y + 1, v.orientation)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    yield Problem(new_vehicles)

def load_file(file):
    vehicles = []
    for line in file:
        line = line.strip()
        if not line: continue
        id, x, y, orientation = line
        vehicles.append(Vehicle(id, int(x), int(y), orientation))
    return Problem(set(vehicles))

def solution_steps(solution):
    steps = []
    for i in range(len(solution) - 1):
        v1 = list(solution[i].vehicles - solution[i+1].vehicles)[0]
        v2 = list(solution[i+1].vehicles - solution[i].vehicles)[0]
        if v1.x < v2.x: steps.append(f'{v1.id}R')
        elif v1.x > v2.x: steps.append(f'{v1.id}L')
        elif v1.y < v2.y: steps.append(f'{v1.id}D')
        elif v1.y > v2.y: steps.append(f'{v1.id}U')
    return steps

if __name__ == '__main__':
    import sys
    from solver import ucs

    with open(sys.argv[1]) as f:
        problem = load_file(f)

    result = ucs(problem)
    print(f"Found {len(result['solutions'])} solutions.")
    for solution in result['solutions']:
        print(" → ".join(solution_steps(solution)))
