
class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.f = 0
        self.g = 0
        self.h = 0

    def __eq__(self, other):
            return self.position == other.position
    def __hash__(self):
        return hash(self.position)