CAR_IDS = {'X', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'}
TRUCK_IDS = {'O', 'P', 'Q', 'R'}

class Vehicle:

    def __init__(self, id, x, y, orientation):
        if id in CAR_IDS:
            self.id = id
            self.length = 2
        elif id in TRUCK_IDS:
            self.id = id
            self.length = 3
        else:
            raise ValueError(f'Invalid id {id}')

        if 0 <= x <= 5:
            self.x = x
        else:
            raise ValueError(f'Invalid x {x}')

        if 0 <= y <= 5:
            self.y = y
        else:
            raise ValueError(f'Invalid y {y}')

        if orientation == 'H':
            self.orientation = orientation
            if x + self.length - 1 > 5:
                raise ValueError('Vehicle exceeds board horizontally')
        elif orientation == 'V':
            self.orientation = orientation
            if y + self.length - 1 > 5:
                raise ValueError('Vehicle exceeds board vertically')
        else:
            raise ValueError(f'Invalid orientation {orientation}')

    def __hash__(self):
        return hash((self.id, self.x, self.y, self.orientation))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __lt__(self, other):
        return self.id < other.id

    def __repr__(self):
        return f"Vehicle({self.id}, {self.x}, {self.y}, {self.orientation})"
