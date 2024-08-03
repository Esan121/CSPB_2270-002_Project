class HalfEdge:
    def __init__(self, origin, twin, next, prev):
        self.origin = origin
        self.twin = twin
        self.next = next
        self.prev = prev

class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Face:
    def __init__(self, outer_component):
        self.outer_component = outer_component