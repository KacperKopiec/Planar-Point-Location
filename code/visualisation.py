from data_structures.Point import Point
from data_structures.Segment import Segment
from data_structures.Trapezoid import Trapezoid
from data_structures.TrapezoidalMap import TrapezoidalMap
import matplotlib.pyplot as plt
from PIL import Image
import io
from drawApplication import *
from examples import *


def showMap(map: TrapezoidalMap, Trapezoids: list[Trapezoid], lines: list[Segment], q: Point = None):
    plt.figure(figsize = (5,5))
    plt.axis("off")
    for line in lines:
        plt.plot([line.left.x, line.right.x], [ line.left.y, line.right.y], color = "blue")
    for trapez in Trapezoids:
        A,B,C,D = trapez.trapezoidBoundary()
        plt.plot([A.x, B.x], [A.y, B.y], color = "green")
        plt.plot([C.x, D.x], [C.y, D.y], color = "green")
    A,B,C,D = map.createBoundary().trapezoidBoundary()
    plt.plot([A.x, B.x], [A.y, B.y], color = "black")
    plt.plot([C.x, D.x], [C.y, D.y], color = "black")
    plt.plot([A.x, C.x], [A.y, C.y], color = "black")
    plt.plot([B.x, D.x], [B.y, D.y], color = "black")

    if q is not None: 
        plt.scatter([q.x],[q.y], color = "red")
        found = map.query(q).data
        A,B,C,D = found.trapezoidBoundary()
        plt.plot([A.x, B.x], [A.y, B.y], color = "red")
        plt.plot([C.x, D.x], [C.y, D.y], color = "red")
        plt.plot([A.x, C.x], [A.y, C.y], color = "red")
        plt.plot([B.x, D.x], [B.y, D.y], color = "red")

    plt.show()

def mapBuildingSteps(segments: list[Segment],q : Point = None, random=True):
    T = TrapezoidalMap(segments, visualisation=True, random=random)
    for s in range(len(T.frames)):
        showMap(T, T.frames[s], T.segments[:s])
    # showMap()

def makeGif(segments: list[Segment], name : str = "Przyklad", q: Point = None, random=True):
    T = TrapezoidalMap(segments, visualisation=True, random=random)
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
            if q is not None: 
                plt.scatter([q.x],[q.y], color = "red")
                found = T.query(q).data
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
    frames[0].save(f'../gify/{name}.gif', save_all=True, append_images=frames[1:], duration=500, loop=0)
    
def drawAndSave(name: str = "test"):
    segments,q = draw()
    T = TrapezoidalMap(segments,True)
    showMap(T,T.frames[-1],T.segments,q)
    with open(f"../trapezy/{name}.txt", "w") as plik:  
        plik.write("Zadane Segmenty: \n")
        for seg in segments:
            plik.write(f"{seg}")
        plik.write("\nUtworzone Trapezy: \n")
        for trapez in T.frames[-1]:
            plik.write(f"{trapez}\n")
        if q is not None:
            plik.write(f"Trapez w którym jest punkt: \n{T.query(q).data}")
    plik.close()
    return T,q

def fromFile(segments: list[Segment],q:Point = None, name: str = "test"):
    T = TrapezoidalMap(segments,True)
    showMap(T,T.frames[-1],T.segments,q)
    with open(f"../trapezy/{name}.txt", "w") as plik:  
        plik.write("Zadane Segmenty: \n")
        for seg in segments:
            plik.write(f"{seg}")
        plik.write("\nUtworzone Trapezy: \n")
        for trapez in T.frames[-1]:
            plik.write(f"{trapez}\n")
        if q is not None:
            plik.write(f"Trapez w którym jest punkt: \n{T.query(q).data}")
    plik.close()
    return T,q

def showMapInteractive(map: TrapezoidalMap, Trapezoids: list[Trapezoid], lines: list[Segment]):
    def on_move(event):
        if event.inaxes:
            A,B,C,D = map.createBoundary().trapezoidBoundary()
            q = Point(event.xdata, event.ydata)
            if A.x <= q.x <= C.x and A.y <= q.y <= B.y:
                plt.clf()
                plt.axis("off")
                for line in lines:
                    plt.plot([line.left.x, line.right.x], [ line.left.y, line.right.y], color = "blue")
                for trapez in Trapezoids:
                    A,B,C,D = trapez.trapezoidBoundary()
                    plt.plot([A.x, B.x], [A.y, B.y], color = "green")
                    plt.plot([C.x, D.x], [C.y, D.y], color = "green")
                A,B,C,D = map.createBoundary().trapezoidBoundary()
                plt.plot([A.x, B.x], [A.y, B.y], color = "black")
                plt.plot([C.x, D.x], [C.y, D.y], color = "black")
                plt.plot([A.x, C.x], [A.y, C.y], color = "black")
                plt.plot([B.x, D.x], [B.y, D.y], color = "black")

                plt.scatter([q.x],[q.y], color = "red")

                found = map.query(q).data
                A,B,C,D = found.trapezoidBoundary()
                plt.plot([A.x, B.x], [A.y, B.y], color = "red")
                plt.plot([C.x, D.x], [C.y, D.y], color = "red")
                plt.plot([A.x, C.x], [A.y, C.y], color = "red")
                plt.plot([B.x, D.x], [B.y, D.y], color = "red")

                plt.draw()
            else:
                plt.clf()
                plt.axis("off")
                for line in lines:
                    plt.plot([line.left.x, line.right.x], [ line.left.y, line.right.y], color = "blue")
                for trapez in Trapezoids:
                    A,B,C,D = trapez.trapezoidBoundary()
                    plt.plot([A.x, B.x], [A.y, B.y], color = "green")
                    plt.plot([C.x, D.x], [C.y, D.y], color = "green")
                A,B,C,D = map.createBoundary().trapezoidBoundary()
                plt.plot([A.x, B.x], [A.y, B.y], color = "black")
                plt.plot([C.x, D.x], [C.y, D.y], color = "black")
                plt.plot([A.x, C.x], [A.y, C.y], color = "black")
                plt.plot([B.x, D.x], [B.y, D.y], color = "black")

                plt.draw()


    plt.figure(figsize = (5,5))
    plt.axis("off")
    for line in lines:
        plt.plot([line.left.x, line.right.x], [ line.left.y, line.right.y], color = "blue")
    for trapez in Trapezoids:
        A,B,C,D = trapez.trapezoidBoundary()
        plt.plot([A.x, B.x], [A.y, B.y], color = "green")
        plt.plot([C.x, D.x], [C.y, D.y], color = "green")
    A,B,C,D = map.createBoundary().trapezoidBoundary()
    plt.plot([A.x, B.x], [A.y, B.y], color = "black")
    plt.plot([C.x, D.x], [C.y, D.y], color = "black")
    plt.plot([A.x, C.x], [A.y, C.y], color = "black")
    plt.plot([B.x, D.x], [B.y, D.y], color = "black")

    plt.connect('motion_notify_event', on_move)
    plt.show(block=True)