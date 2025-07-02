import sys
from vehicle import Vehicle
from solver import bfs

GOAL_VEHICLE = Vehicle('X', 4, 2, 'H')

class Problem(object):
    """A configuration of a single Rush Hour board."""

    def __init__(self, vehicles):
        """Create a new Rush Hour board.
        
        Arguments:
            vehicles: a set of Vehicle objects.
        """
        self.vehicles = vehicles

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return self.vehicles == other.vehicles

    def __ne__(self, other):
        return not self.__eq__(other)

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
                    board[y][x+i] = vehicle.id
            else:
                for i in range(vehicle.length):
                    board[y+i][x] = vehicle.id
        return board

    def solved(self):
        """Returns true if the board is in a solved state."""
        return GOAL_VEHICLE in self.vehicles

    def moves(self):
        """Return iterator of next possible moves."""
        board = self.get_board()
        for v in self.vehicles:
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
        r1, r2 = solution[i], solution[i+1]
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

    results = bfs(problem, max_depth=100)

    print('{0} Solutions found'.format(len(results['solutions'])))
    for solution in results['solutions']:
        print('Solution: {0}'.format(', '.join(solution_steps(solution))))

    print('{0} Nodes visited'.format(len(results['visited'])))
