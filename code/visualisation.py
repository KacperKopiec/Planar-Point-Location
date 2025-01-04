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
        bottom = trapez.bottom
        top = trapez.top
        left = trapez.left
        right = trapez.right
        if bottom.point_over_segment(left) == 0:
            A = left
            B = top.value_for_x(left.x)
        else:
            A = bottom.value_for_y(left.x)
            B = left
        if bottom.point_over_segment(right) == 0:
            C = right
            D = top.value_for_x(right.x)
        else:
            C = top.value_for_x(right.x)
            D = right
        plt.plot([A.x, B.x], [A.y, B.y], color = "green")
        plt.plot([C.x, D.x], [C.y, D.y], color = "green")

    plt.show()



    