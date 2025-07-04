import copy

class Vehicle:
    def __init__(self, vid, x, y, length, orientation):
        self.id = vid
        self.x = x
        self.y = y
        self.length = length
        self.orientation = orientation  # 'H' or 'V'

    def cells(self):
        return [(self.x + i if self.orientation == 'H' else self.x,
                 self.y + i if self.orientation == 'V' else self.y)
                for i in range(self.length)]

    def move(self, direction):
        if self.orientation == 'H':
            return Vehicle(self.id, self.x + direction, self.y, self.length, self.orientation)
        else:
            return Vehicle(self.id, self.x, self.y + direction, self.length, self.orientation)

    def __eq__(self, other):
        return (self.id, self.x, self.y) == (other.id, other.x, other.y)

    def __hash__(self):
        return hash((self.id, self.x, self.y))

class State:
    def __init__(self, vehicles, size=6):
        self.size = size
        self.vehicles = {v.id: v for v in vehicles}
        self.grid = [['.' for _ in range(size)] for _ in range(size)]
        for v in vehicles:
            for x, y in v.cells():
                self.grid[y][x] = v.id
        self.key = self._generate_key()

    def _generate_key(self):
        return tuple((v.id, v.x, v.y) for v in sorted(self.vehicles.values(), key=lambda v: v.id))

    def is_goal(self):
        red = self.vehicles['X']
        return red.orientation == 'H' and red.x + red.length == self.size

    def get_moves(self):
        next_states = []
        for vid, v in self.vehicles.items():
            for d in [-1, 1]:
                moved = v.move(d)
                valid = True
                for x, y in moved.cells():
                    if not (0 <= x < self.size and 0 <= y < self.size):
                        valid = False
                        break
                    if (x, y) not in v.cells() and self.grid[y][x] != '.':
                        valid = False
                        break
                if valid:
                    new_vehicles = copy.deepcopy(list(self.vehicles.values()))
                    for i in range(len(new_vehicles)):
                        if new_vehicles[i].id == vid:
                            new_vehicles[i] = moved
                            break
                    next_states.append((State(new_vehicles, self.size), v.length))
        return next_states

    def __eq__(self, other):
        return self.key == other.key

    def __hash__(self):
        return hash(self.key)

    def __lt__(self, other):
        return False  # required for heapq
