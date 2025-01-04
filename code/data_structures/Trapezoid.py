from Point import Point
from Segment import Segment

class Trapezoid:
    def __init__(self, left: Point, right: Point, top: Segment, bottom: Segment):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        
        self.nextUp = None
        self.nextDown = None

    def __hash__(self):
        return hash((self.left, self.right))
    
    def __str__(self):
        return f"lp:[{self.left}], rp:[{self.right}], top:[{self.top}], bot:[{self.bottom}]"