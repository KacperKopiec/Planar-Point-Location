from data_structures.Point import Point
from data_structures.Segment import Segment
from data_structures.Trapezoid import Trapezoid
import matplotlib.pyplot as plt



def show_map(Trapezoids : list[Trapezoid] , lines : list[Segment], q : Point, found : Trapezoid  ):
    plt.figure(figsize = (5,5))
    plt.axis("off")
    plt.scatter([q.x],[q.y], color = "red")
    for line in lines:
        plt.plot([line.left.x, line.right.x], [ line.left.y, line.right.y], color = "blue")
    for trapez in Trapezoids:
        A,B,C,D = trapez.trapezoidBoundary()
        plt.plot([A.x, B.x], [A.y, B.y], color = "green")
        plt.plot([C.x, D.x], [C.y, D.y], color = "green")
    A,B,C,D = found.trapezoidBoundary()
    plt.plot([A.x, B.x], [A.y, B.y], color = "red")
    plt.plot([C.x, D.x], [C.y, D.y], color = "red")
    plt.plot([A.x, C.x], [A.y, C.y], color = "red")
    plt.plot([B.x, D.x], [B.y, D.y], color = "red")