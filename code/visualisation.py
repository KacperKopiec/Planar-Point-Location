from data_structures.Point import Point
from data_structures.Segment import Segment
from data_structures.Trapezoid import Trapezoid
from data_structures.TrapezoidalMap import Trapezoidal_map
import matplotlib.pyplot as plt


def show_map(map: Trapezoidal_map, Trapezoids: list[Trapezoid], lines: list[Segment], q: Point = None, found: Trapezoid = None):
    plt.figure(figsize = (5,5))
    plt.axis("off")
    for line in lines:
        plt.plot([line.left.x, line.right.x], [ line.left.y, line.right.y], color = "blue")
    for trapez in Trapezoids:
        A,B,C,D = trapez.trapezoidBoundary()
        plt.plot([A.x, B.x], [A.y, B.y], color = "green")
        plt.plot([C.x, D.x], [C.y, D.y], color = "green")
    A,B,C,D = map.createBoundary().trapezoidBoundary()
    plt.plot([A.x, B.x], [A.y, B.y], color = "green")
    plt.plot([C.x, D.x], [C.y, D.y], color = "green")
    plt.plot([A.x, C.x], [A.y, C.y], color = "green")
    plt.plot([B.x, D.x], [B.y, D.y], color = "green")

    if q != None: plt.scatter([q.x],[q.y], color = "red")
    if found != None:
        A,B,C,D = found.trapezoidBoundary()
        plt.plot([A.x, B.x], [A.y, B.y], color = "red")
        plt.plot([C.x, D.x], [C.y, D.y], color = "red")
        plt.plot([A.x, C.x], [A.y, C.y], color = "red")
        plt.plot([B.x, D.x], [B.y, D.y], color = "red")

    plt.show()