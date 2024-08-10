class HalfEdge:
    def __init__(self, origin, twin=None, next=None, prev=None, face=None):
        self.origin = origin
        self.twin = twin
        self.next = next
        self.prev = prev
        self.face = face

class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Face:
    def __init__(self, outer_component):
        self.outer_component = outer_component