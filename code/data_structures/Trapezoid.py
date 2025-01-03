import Point, Segment

class Trapezoid:
    def __init__(self, left: Point, right: Point, top: Segment, bottom: Segment):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    def __hash__(self):
        return hash((self.left, self.right))