from data_structures.Point import Point
from data_structures.Segment import Segment
from data_structures.Trapezoid import Trapezoid
import matplotlib.pyplot as plt

def show_map(Trapezoids : list[Trapezoid] , lines : list[Segment]):
    plt.figure(figsize = (5,5))
    plt.axis("off")
    for line in lines:
        plt.plot([line.left.x, line.right.x], [ line.left.y, line.right.y], color = "blue")
    for trapez in Trapezoids:
        plt.plot([trapez.top.left.x, trapez.bottom.left.x], [trapez.top.left.y, trapez.bottom.left.y], color = "green")
    plt.show()
