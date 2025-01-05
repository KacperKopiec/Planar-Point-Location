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
        self.trapezoids = set([self.root.data])
        for s in permutation(self.segment):
            intersections = self.intersectingTrapezoids(s)
            if len(intersections) == 1:
                self.__changeOne(intersections[0], s)
            else:
                self.__changeMoreThanOne(intersections, s)

    def createBoundary(self):
        x_mn, y_mn, x_mx, y_mx = float('inf'), float('inf'), float('-inf'), float('-inf')
        for s in self.segment:
            x_mn = min(x_mn, s.left.x, s.right.x)
            x_mx = max(x_mx, s.left.x, s.right.x)
            y_mn = min(y_mn, s.left.y, s.right.y)
            y_mx = max(y_mx, s.left.y, s.right.y)
        
        lpoint, rpoint = Point(x_mn, y_mx), Point(x_mx, y_mx)
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

    def intersectingTrapezoids(self, segment: Segment):
        p = Point(segment.left.x, segment.left.y)
        cur = self.query(p)
        leaves = []
        while p.x < segment.right.x:
            leaves.append(cur)
            p.x = cur.data.right.x
            p.y = segment.value_for_x(p.x)
            if cur.data.nextUp == None: break
            if cur.data.nextUp.data.bottom.point_over_segment(p) == 1:
                cur = cur.data.nextUp
            else:
                cur = cur.data.nextDown
        return leaves

    def __changeOne(self, node: TrapezoidNode, segment: Segment):
        nd = PointNode(segment.left)
        nd.setLeft(TrapezoidNode(Trapezoid(node.data.left, segment.left, node.data.top, node.data.bottom)))
        nd.setRight(PointNode(segment.right))
        nd.right.setLeft(SegmentNode(segment))
        nd.right.left.setLeft(TrapezoidNode(Trapezoid(segment.left, segment.right, node.data.top, segment)))
        nd.right.left.setRight(TrapezoidNode(Trapezoid(segment.left, segment.right, segment, node.data.bottom)))
        nd.right.setRight(TrapezoidNode(Trapezoid(segment.right, node.data.right, node.data.top, node.data.bottom)))

        nd.left.data.nextUp = nd.right.left.left
        nd.left.data.nextDown = nd.right.left.right
        nd.right.left.left.data.nextUp = nd.right.right
        nd.right.left.left.data.nextDown = nd.right.right
        nd.right.left.right.data.nextUp = nd.right.right
        nd.right.left.right.data.nextDown = nd.right.right
        nd.right.right.data.nextUp = node.data.nextUp
        nd.right.right.data.nextDown = node.data.nextDown

        self.trapezoids.remove(node.data)
        self.trapezoids.add(nd.left.data)
        self.trapezoids.add(nd.right.left.left.data)
        self.trapezoids.add(nd.right.left.right.data)
        self.trapezoids.add(nd.right.right.data)
        if len(node.parents) == 0: self.root = nd
        node.replace(nd)

    def __changeMoreThanOne(self, nodes: list[TrapezoidNode], segment: Segment):
        mergeUp = -1
        upTrap, downTrap = None, None
        for idx, node in enumerate(nodes):
            if idx == 0:
                nd = PointNode(segment.left)
                nd.setLeft(TrapezoidNode(Trapezoid(node.data.left, segment.left, node.data.top, node.data.bottom)))
                self.trapezoids.add(nd.left.data)
                upTrap = TrapezoidNode(Trapezoid(segment.left, node.data.right, node.data.top, segment))
                downTrap = TrapezoidNode(Trapezoid(segment.left, node.data.right, segment, node.data.bottom))

                if segment.point_over_segment(node.data.right) == 1:
                    mergeUp = 0
                    downTrap.data.nextUp = node.data.nextUp
                    self.trapezoids.add(upTrap.data)
                else:
                    mergeUp = 1
                    downTrap.data.nextDown = node.data.nextDown
                    self.trapezoids.add(downTrap.data)

                nd.left.data.nextUp = upTrap
                nd.left.data.nextDown = downTrap

                nd.setRight(SegmentNode(segment))
                nd.right.setLeft(upTrap)
                nd.right.setRight(downTrap)

                node.replace(nd)
                self.trapezoids.remove(node.data)
            elif idx == len(nodes) - 1:
                prevUpTrap = upTrap
                prevDownTrap = downTrap

                upTrap = TrapezoidNode(Trapezoid(node.data.left, segment.right, node.data.top, segment))
                downTrap = TrapezoidNode(Trapezoid(node.data.left, segment.right, segment, node.data.bottom))
                Trap = TrapezoidNode(Trapezoid(segment.right, node.data.right, node.data.top, node.data.bottom))

                if mergeUp:
                    prevUpTrap.data.right = node.data.right
                    upTrap = prevUpTrap
                    downTrap.data.nextUp = downTrap
                else:
                    prevDownTrap.data.right = node.data.right
                    downTrap = prevDownTrap
                    upTrap.data.nextDown = upTrap
                
                upTrap.data.nextUp = Trap
                upTrap.data.nextDown = Trap
                downTrap.data.nextUp = Trap
                downTrap.data.nextDown = Trap

                self.trapezoids.add(Trap.data)
                self.trapezoids.add(upTrap.data)
                self.trapezoids.add(downTrap.data)

                nd = PointNode(segment.right)
                nd.setLeft(SegmentNode(segment))
                nd.setRight(Trap)
                nd.left.setLeft(upTrap)
                nd.left.setRight(downTrap)
                node.replace(nd)
                self.trapezoids.remove(node.data)
            else:
                prevUpTrap = upTrap
                prevDownTrap = downTrap

                upTrap = TrapezoidNode(Trapezoid(node.data.left, node.data.right, node.data.top, segment))
                downTrap = TrapezoidNode(Trapezoid(node.data.left, node.data.right, segment, node.data.bottom))

                if mergeUp:
                    prevUpTrap.data.right = node.data.right
                    upTrap = prevUpTrap
                    downTrap.data.nextUp = downTrap
                else:
                    prevDownTrap.data.right = node.data.right
                    downTrap = prevDownTrap
                    upTrap.data.nextDown = upTrap
                
                if segment.point_over_segment(node.data.right) == 1:
                    mergeUp = 0
                    downTrap.data.nextUp = node.data.nextUp
                    self.trapezoids.add(upTrap.data)
                else:
                    mergeUp = 1
                    downTrap.data.nextDown = node.data.nextDown
                    self.trapezoids.add(downTrap.data)

                nd = SegmentNode(segment)
                nd.setLeft(upTrap)
                nd.setRight(downTrap)
                node.replace(nd)
                self.trapezoids.remove(node.data)

    def getTrapezoids(self):
        return list(self.trapezoids)

segments = [
    Segment(Point(0, 0), Point(3, 6)),
    Segment(Point(4, 2), Point(7, 4)),
    Segment(Point(6, 0), Point(10, 6))
]

T = Trapezoidal_map(segments)

print(*T.getTrapezoids(), sep="\n")