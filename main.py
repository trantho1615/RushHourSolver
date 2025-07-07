import sys
from vehicle import Vehicle
from solver import ucs, bfs, dfs, dls, a_star_solver
import time
import tracemalloc




class Problem(object):
    """A configuration of a single Rush Hour board."""

    def __init__(self, vehicles):
        """Create a new Rush Hour board.

        Arguments:
            vehicles: a set of Vehicle objects.
        Goal vehicle ID: X
        """
        self.vehicles = vehicles
        self.goal_vehicle = None
        for v in self.vehicles:
            if v.id == 'X':
                self.goal_vehicle = v
                break

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return self.vehicles == other.vehicles

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return hash(self) < hash(other)

    def __repr__(self):
        s = '-' * 8 + '\n'
        for line in self.get_board():
            s += '|{0}|\n'.format(''.join(line))
        s += '-' * 8 + '\n'
        return s

    def get_board(self):
        """Representation of the Rush Hour board as a 2D list of strings"""
        board = [[' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' ']]
        for vehicle in self.vehicles:
            x, y = vehicle.x, vehicle.y
            if vehicle.orientation == 'H':
                for i in range(vehicle.length):
                    board[y][x + i] = vehicle.id
            else:
                for i in range(vehicle.length):
                    board[y + i][x] = vehicle.id
        return board

    def solved(self):
        for v in self.vehicles:
            if v.id == 'X' and v.orientation == 'H':
                if v.x + v.length - 1 == 5:
                    return True
        return False

    def moves(self):
        """Return iterator of next possible moves."""
        board = self.get_board()
        for v in sorted(list(self.vehicles)):
            if v.orientation == 'H':
                if v.x - 1 >= 0 and board[v.y][v.x - 1] == ' ':
                    new_v = Vehicle(v.id, v.x - 1, v.y, v.orientation)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    yield Problem(new_vehicles)
                if v.x + v.length <= 5 and board[v.y][v.x + v.length] == ' ':
                    new_v = Vehicle(v.id, v.x + 1, v.y, v.orientation)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    yield Problem(new_vehicles)
            else:
                if v.y - 1 >= 0 and board[v.y - 1][v.x] == ' ':
                    new_v = Vehicle(v.id, v.x, v.y - 1, v.orientation)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    yield Problem(new_vehicles)
                if v.y + v.length <= 5 and board[v.y + v.length][v.x] == ' ':
                    new_v = Vehicle(v.id, v.x, v.y + 1, v.orientation)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    yield Problem(new_vehicles)


def load_file(rushhour_file):
    vehicles = []
    for line in rushhour_file:
        line = line[:-1] if line.endswith('\n') else line
        id, x, y, orientation = line
        vehicles.append(Vehicle(id, int(x), int(y), orientation))
    return Problem(set(vehicles))

def solution_steps(solution):
    """Generate list of steps from a solution path."""
    steps = []
    for i in range(len(solution) - 1):
        r1, r2 = solution[i], solution[i + 1]
        v1 = list(r1.vehicles - r2.vehicles)[0]
        v2 = list(r2.vehicles - r1.vehicles)[0]
        if v1.x < v2.x:
            steps.append('{0}R'.format(v1.id))
        elif v1.x > v2.x:
            steps.append('{0}L'.format(v1.id))
        elif v1.y < v2.y:
            steps.append('{0}D'.format(v1.id))
        elif v1.y > v2.y:
            steps.append('{0}U'.format(v1.id))
    return steps


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename) as rushhour_file:
        problem = load_file(rushhour_file)

    algorithm = sys.argv[2] if len(sys.argv) > 2 else 'a*'

    """syntax: python main.py map/p1 a*"""

    tracemalloc.start()
    start_time = time.time()

    if algorithm == 'bfs':
        results = bfs(problem)
    elif algorithm == 'dfs':
        results = dfs(problem)
    elif algorithm == 'ucs':
        results = ucs(problem)
    elif algorithm == 'a*':
        results = a_star_solver(problem)
    elif algorithm == 'dls':
        results =  dls(problem)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"{len(results['solutions'])} Solutions found")
    for solution in results['solutions']:
        print('Solution:', ', '.join(solution_steps(solution)))

    print(f"{len(results['visited'])} Nodes visited")
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    print(f"Peak memory used: {peak / 1024:.2f} KB")