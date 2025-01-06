from data_structures.Point import Point
from data_structures.Segment import Segment
from data_structures.Trapezoid import Trapezoid
from data_structures.PointNode import PointNode
from data_structures.SegmentNode import SegmentNode
from data_structures.TrapezoidNode import TrapezoidNode
from numpy.random import permutation
from math import ceil

class TrapezoidalMap:
    def __init__(self, segments: list[Segment]):
        self.segments = permutation(segments)
        self.root = TrapezoidNode(self.createBoundary())
        self.trapezoids = set([self.root.data])
        self.frames = [self.getTrapezoids()]
        for i, s in enumerate(self.segments):
            intersections = self.intersectingTrapezoids(s)
            if len(intersections) == 1:
                self.changeOne(intersections[0], s)
            else:
                self.changeMoreThanOne(intersections, s)
            # self.frames.append(self.getTrapezoids())

    def createBoundary(self):
        x_mn, y_mn, x_mx, y_mx = float('inf'), float('inf'), float('-inf'), float('-inf')
        for s in self.segments:
            x_mn = min(x_mn, s.left.x, s.right.x)
            x_mx = max(x_mx, s.left.x, s.right.x)
            y_mn = min(y_mn, s.left.y, s.right.y)
            y_mx = max(y_mx, s.left.y, s.right.y)
        
        diff_x, diff_y = ceil((x_mx - x_mn) / 100 * 10), ceil((y_mx - y_mn) / 100 * 10)
        x_mn -= diff_x
        x_mx += diff_x
        y_mn -= diff_y
        y_mx += diff_y

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
                if cur.data.point_over_segment(p) == 1:
                    cur = cur.left
                else:
                    cur = cur.right
        return cur

    def intersectingTrapezoids(self, segment: Segment):
        p = Point(segment.left.x, segment.left.y)
        cur = self.query(p)
        leaves = [cur]
        p = segment.value_for_x(cur.data.right.x)
        while p.x < segment.right.x:
            if cur.data.nextUp.data.bottom.point_over_segment(p) == 1:
                cur = cur.data.nextUp
            else:
                cur = cur.data.nextDown
            leaves.append(cur)
            p = segment.value_for_x(cur.data.right.x)
        return leaves

    def changeOne(self, node: TrapezoidNode, segment: Segment):
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

        nd.right.right.data.prevUp = nd.right.left.left
        nd.right.right.data.prevDown = nd.right.left.right
        nd.right.left.left.data.prevUp = nd.left
        nd.right.left.left.data.prevDown = nd.left
        nd.right.left.right.data.prevUp = nd.left
        nd.right.left.right.data.prevDown = nd.left
        nd.left.data.prevDown = node.data.prevDown
        nd.left.data.prevUp = node.data.prevUp

        if node.data.prevUp != None and node.data.prevUp.data.nextDown is node: 
            if node.data.prevUp.data.nextDown == node.data.prevUp.data.nextUp:
                node.data.prevUp.data.nextUp = nd.left
            node.data.prevUp.data.nextDown = nd.left
        if node.data.prevDown != None and node.data.prevDown.data.nextUp is node: 
            if node.data.prevDown.data.nextDown == node.data.prevDown.data.nextUp:
                node.data.prevDown.data.nextDown = nd.left
            node.data.prevDown.data.nextUp = nd.left
        if node.data.nextUp != None and node.data.nextUp.data.prevDown is node: 
            if node.data.nextUp.data.prevUp == node.data.nextUp.data.prevDown:
                node.data.nextUp.data.prevUp = nd.right.right
            node.data.nextUp.data.prevDown = nd.right.right
        if node.data.nextDown != None and node.data.nextDown.data.prevUp is node:
            if node.data.nextDown.data.prevDown == node.data.nextDown.data.prevUp:
                node.data.nextDown.data.prevDown = nd.right.right
            node.data.nextDown.data.prevUp = nd.right.right

        self.trapezoids.remove(node.data)
        self.trapezoids.add(nd.left.data)
        self.trapezoids.add(nd.right.left.left.data)
        self.trapezoids.add(nd.right.left.right.data)
        self.trapezoids.add(nd.right.right.data)
        if len(node.parents) == 0: self.root = nd
        node.replace(nd)

    def changeMoreThanOne(self, nodes: list[TrapezoidNode], segment: Segment):
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
                    self.trapezoids.add(upTrap.data)
                else:
                    mergeUp = 1
                    self.trapezoids.add(downTrap.data)

                nd.left.data.nextUp = upTrap
                nd.left.data.nextDown = downTrap
                nd.left.data.prevUp = node.data.prevUp
                nd.left.data.prevDown = node.data.prevDown
                upTrap.data.prevUp = nd.left
                upTrap.data.prevDown = nd.left
                downTrap.data.prevUp = nd.left
                downTrap.data.prevDown = nd.left
                if node.data.prevUp != None and node.data.prevUp.data.nextDown is node: 
                    if node.data.prevUp.data.nextDown == node.data.prevUp.data.nextUp:
                        node.data.prevUp.data.nextUp = nd.left
                    node.data.prevUp.data.nextDown = nd.left
                if node.data.prevDown != None and node.data.prevDown.data.nextUp is node: 
                    if node.data.prevDown.data.nextUp == node.data.prevDown.data.nextDown:
                        node.data.prevDown.data.nextDown = nd.left
                    node.data.prevDown.data.nextUp = nd.left

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
                    prevUpTrap.data.right = segment.right
                    upTrap = prevUpTrap
                    prevDownTrap.data.nextUp = downTrap
                    downTrap.data.prevUp = prevDownTrap
                    
                    p1 = prevDownTrap.data.bottom.value_for_x(downTrap.data.left.x)
                    p2 = downTrap.data.bottom.value_for_x(downTrap.data.left.x)

                    if p1.y < p2.y:
                        downTrap.data.prevDown = prevDownTrap
                        prevDownTrap.data.nextUp = downTrap
                        prevDownTrap.data.nextDown = nodes[idx - 1].data.nextDown
                        if nodes[idx - 1].data.nextDown != None: 
                            if nodes[idx - 1].data.nextDown.data.prevUp == nodes[idx - 1].data.nextDown.data.prevDown:
                                nodes[idx - 1].data.nextDown.data.prevDown = prevDownTrap
                            nodes[idx - 1].data.nextDown.data.prevUp = prevDownTrap
                    elif p1.y > p2.y:
                        prevDownTrap.data.nextDown = downTrap
                        downTrap.data.prevUp = prevDownTrap
                        downTrap.data.prevDown = node.data.prevDown
                        if node.data.prevDown != None:
                            if node.data.prevDown.data.nextUp == node.data.prevDown.data.nextDown:
                                node.data.prevDown.data.nextDown = downTrap
                            node.data.prevDown.data.nextUp = downTrap
                    else:
                        prevDownTrap.data.nextDown = downTrap
                        downTrap.data.prevDown = prevDownTrap
                else:
                    prevDownTrap.data.right = segment.right
                    downTrap = prevDownTrap
                    prevUpTrap.data.nextDown = upTrap
                    upTrap.data.prevDown = prevUpTrap

                    p1 = prevUpTrap.data.top.value_for_x(upTrap.data.left.x)
                    p2 = upTrap.data.top.value_for_x(upTrap.data.left.x)

                    if p1.y > p2.y:
                        upTrap.data.prevUp = prevUpTrap
                        prevUpTrap.data.nextUp = nodes[idx - 1].data.nextUp
                        if nodes[idx - 1].data.nextUp != None: 
                            if nodes[idx - 1].data.nextUp.data.prevDown == nodes[idx - 1].data.nextUp.data.prevUp:
                                nodes[idx - 1].data.nextUp.data.prevUp = prevUpTrap
                            nodes[idx - 1].data.nextUp.data.prevDown = prevUpTrap
                    elif p1.y < p2.y:
                        prevUpTrap.data.nextUp = upTrap
                        upTrap.data.prevUp = node.data.prevUp
                        if node.data.prevUp != None: 
                            if node.data.prevUp.data.nextUp == node.data.prevUp.data.nextDown:
                                node.data.prevUp.data.nextUp = upTrap
                            node.data.prevUp.data.nextDown = upTrap
                    else:
                        prevUpTrap.data.nextUp = upTrap
                        upTrap.data.prevUp = prevUpTrap
                
                upTrap.data.nextUp = Trap
                upTrap.data.nextDown = Trap
                downTrap.data.nextUp = Trap
                downTrap.data.nextDown = Trap
                Trap.data.prevUp = upTrap
                Trap.data.prevDown = downTrap
                Trap.data.nextUp = node.data.nextUp
                Trap.data.nextDown = node.data.nextDown
                if node.data.nextUp != None and node.data.nextUp.data.prevDown is node: 
                    if node.data.nextUp.data.prevDown == node.data.nextUp.data.prevUp:
                        node.data.nextUp.data.prevUp = Trap
                    node.data.nextUp.data.prevDown = Trap
                if node.data.nextDown != None and node.data.nextDown.data.prevUp is node: 
                    if node.data.nextDown.data.prevUp == node.data.nextDown.data.prevDown:
                        node.data.nextDown.data.prevDown = Trap
                    node.data.nextDown.data.prevUp = Trap

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
                    prevDownTrap.data.nextUp = downTrap
                    downTrap.data.prevUp = prevDownTrap
                    
                    p1 = prevDownTrap.data.bottom.value_for_x(downTrap.data.left.x)
                    p2 = downTrap.data.bottom.value_for_x(downTrap.data.left.x)

                    if p1.y < p2.y:
                        downTrap.data.prevDown = prevDownTrap
                        prevDownTrap.data.nextUp = downTrap
                        prevDownTrap.data.nextDown = nodes[idx - 1].data.nextDown
                        if nodes[idx - 1].data.nextDown != None: 
                            if nodes[idx - 1].data.nextDown.data.prevUp == nodes[idx - 1].data.nextDown.data.prevDown:
                                nodes[idx - 1].data.nextDown.data.prevDown = prevDownTrap
                            nodes[idx - 1].data.nextDown.data.prevUp = prevDownTrap
                    elif p1.y > p2.y:
                        prevDownTrap.data.nextDown = downTrap
                        downTrap.data.prevUp = prevDownTrap
                        downTrap.data.prevDown = node.data.prevDown
                        if node.data.prevDown != None:
                            if node.data.prevDown.data.nextUp == node.data.prevDown.data.nextDown:
                                node.data.prevDown.data.nextDown = downTrap
                            node.data.prevDown.data.nextUp = downTrap
                    else:
                        prevDownTrap.data.nextDown = downTrap
                        downTrap.data.prevDown = prevDownTrap
                else:
                    prevDownTrap.data.right = node.data.right
                    downTrap = prevDownTrap
                    prevUpTrap.data.nextDown = upTrap
                    upTrap.data.prevDown = prevUpTrap

                    p1 = prevUpTrap.data.top.value_for_x(upTrap.data.left.x)
                    p2 = upTrap.data.top.value_for_x(upTrap.data.left.x)

                    if p1.y > p2.y:
                        upTrap.data.prevUp = prevUpTrap
                        prevUpTrap.data.nextUp = nodes[idx - 1].data.nextUp
                        if nodes[idx - 1].data.nextUp != None: 
                            if nodes[idx - 1].data.nextUp.data.prevDown == nodes[idx - 1].data.nextUp.data.prevUp:
                                nodes[idx - 1].data.nextUp.data.prevUp = prevUpTrap
                            nodes[idx - 1].data.nextUp.data.prevDown = prevUpTrap
                    elif p1.y < p2.y:
                        prevUpTrap.data.nextUp = upTrap
                        upTrap.data.prevUp = node.data.prevUp
                        if node.data.prevUp != None: 
                            if node.data.prevUp.data.nextUp == node.data.prevUp.data.nextDown:
                                node.data.prevUp.data.nextUp = upTrap
                            node.data.prevUp.data.nextDown = upTrap
                    else:
                        prevUpTrap.data.nextUp = upTrap
                        upTrap.data.prevUp = prevUpTrap

                
                if segment.point_over_segment(node.data.right) == 1:
                    mergeUp = 0
                    self.trapezoids.add(upTrap.data)
                else:
                    mergeUp = 1
                    self.trapezoids.add(downTrap.data)

                nd = SegmentNode(segment)
                nd.setLeft(upTrap)
                nd.setRight(downTrap)
                node.replace(nd)
                self.trapezoids.remove(node.data)

    def getTrapezoids(self):
        return list(self.trapezoids)