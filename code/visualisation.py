from data_structures.Point import Point
from data_structures.Segment import Segment
from data_structures.Trapezoid import Trapezoid
from data_structures.TrapezoidalMap import TrapezoidalMap
import matplotlib.pyplot as plt
from PIL import Image
import io


def showMap(map: TrapezoidalMap, Trapezoids: list[Trapezoid], lines: list[Segment], q: Point = None, found: Trapezoid = None):
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

    if q is not None: plt.scatter([q.x],[q.y], color = "red")
    if found is not None:
        A,B,C,D = found.trapezoidBoundary()
        plt.plot([A.x, B.x], [A.y, B.y], color = "red")
        plt.plot([C.x, D.x], [C.y, D.y], color = "red")
        plt.plot([A.x, C.x], [A.y, C.y], color = "red")
        plt.plot([B.x, D.x], [B.y, D.y], color = "red")

    plt.show()

def mapBuildingSteps(segments: list[Segment]):
    T = TrapezoidalMap(segments)
    for s in range(len(T.frames)):
        showMap(T, T.frames[s], T.segments[:s])

def makeGif(segments: list[Segment], name : str, q: Point):
    T = TrapezoidalMap(segments)
    frames = []
    for s in range(len(T.frames)):
        fig,ax = plt.subplots(figsize = (5,5))
        ax.axis("off")
        for line in T.segments[:s]:
            ax.plot([line.left.x, line.right.x], [ line.left.y, line.right.y], color = "blue")
        for trapez in T.frames[s]:
            A,B,C,D = trapez.trapezoidBoundary()
            ax.plot([A.x, B.x], [A.y, B.y], color = "green")
            ax.plot([C.x, D.x], [C.y, D.y], color = "green")
        A,B,C,D = T.createBoundary().trapezoidBoundary()
        ax.plot([A.x, B.x], [A.y, B.y], color = "green")
        ax.plot([C.x, D.x], [C.y, D.y], color = "green")
        ax.plot([A.x, C.x], [A.y, C.y], color = "green")
        ax.plot([B.x, D.x], [B.y, D.y], color = "green")
        if s == len(T.frames)-1:
            found = T.query(q).data
            print(q)
            if q is not None: plt.scatter([q.x],[q.y], color = "red")
            if found is not None:
                A,B,C,D = found.trapezoidBoundary()
                plt.plot([A.x, B.x], [A.y, B.y], color = "red")
                plt.plot([C.x, D.x], [C.y, D.y], color = "red")
                plt.plot([A.x, C.x], [A.y, C.y], color = "red")
                plt.plot([B.x, D.x], [B.y, D.y], color = "red")
        buf = io.BytesIO()
        fig.savefig(buf, format='PNG')
        buf.seek(0)
        frames.append(Image.open(buf)) 
        plt.close(fig)
    frames[0].save(f'../gify/{name}.gif', save_all=True, append_images=frames[1:], duration=200, loop=0)
    