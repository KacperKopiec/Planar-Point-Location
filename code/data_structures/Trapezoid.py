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

    def trapezoidBoundary(self):
        bottom = self.bottom
        top = self.top
        left = self.left
        right = self.right
        A = bottom.value_for_x(left.x)
        B = top.value_for_x(left.x)
        C = bottom.value_for_x(right.x)
        D = top.value_for_x(right.x)
        return A,B,C,D

    def __hash__(self):
        return hash((self.left, self.right, self.top, self.bottom))
    
    def __str__(self):
        return f"lp:[{self.left}], rp:[{self.right}], top:[{self.top}], bot:[{self.bottom}]"