from Point import Point
from Segment import Segment
from Trapezoid import Trapezoid
from PointNode import PointNode
from SegmentNode import SegmentNode
from TrapezoidNode import TrapezoidNode
from numpy.random import permutation

class Trapezoidal_map:
    def __init__(self, segments: list[Segment]):
        self.segment = segments
        self.root = TrapezoidNode(self.createBoundary())
        for s in permutation(self.segment):
            break

    def createBoundary(self):
        x_mn, y_mn, x_mx, y_mx = float('inf'), float('inf'), float('-inf'), float('-inf')
        for s in self.segment:
            x_mn = min(x_mn, s.left.x, s.right.x)
            x_mx = max(x_mx, s.left.x, s.right.x)
            y_mn = min(y_mn, s.left.y, s.right.y)
            y_mx = max(y_mx, s.left.y, s.right.y)
        
        lpoint, rpoint = Point(x_mn, y_mn), Point(x_mx, y_mx)
        botsegment, topsegment = Segment(Point(x_mn, y_mn), Point(x_mx, y_mn)), Segment(Point(x_mn, y_mx), Point(x_mx, y_mx))
        return Trapezoid(lpoint, rpoint, topsegment, botsegment)
    
    def query(self, p: Point):
        cur = self.root
        while cur.getType() != 2:
            if cur.getType() == 0:
                if p < cur.data:
                    cur = cur.left
                else:
                    cur = cur.right
            else:
                if cur.data.point_over_segment(p):
                    cur = cur.left
                else:
                    cur = cur.right
        return cur

    def intersectingTrapezoids(self, segment):
        pass

    def __changeOne(self):
        pass

    def __changeMoreThanOne(self):
        pass    

segments = [
    Segment(Point(0, 0), Point(3, 6)),
    Segment(Point(4, 2), Point(7, 4)),
    Segment(Point(6, 0), Point(10, 6))
]

T = Trapezoidal_map(segments)

print(T.query(Point(3, 3)).data)