import numpy as np
from examples import *
from visualisation import *
from data_structures.TrapezoidalMap import *
import time

def randomPoint(mapa : TrapezoidalMap):
    trapez = mapa.createBoundary()
    A,B,C,D = trapez.trapezoidBoundary()
    return Point(np.random.uniform(A.x,D.x),np.random.uniform(A.y-1,B.y))
def generateSegment(n: int,a: int = 0,b: int = 1000):
    X = set()
    Y = set()
    segments = []
    count = 0
    while count<n:
        y = np.random.uniform(a,b)
        if y in Y:
            continue
        a_x = np.random.uniform(a,b)
        if a_x in X:
            continue
        b_x = np.random.uniform(a,b)
        if b_x in X or b_x==a_x:
            continue
        if a_x > b_x:
            a_x,b_x = b_x,a_x
        segments.append(Segment(Point(a_x,y),Point(b_x,y)))
        X.add(a_x)
        X.add(b_x)
        Y.add(y)
        count+=1
    return segments

def test(segments: list[Segment],flag: bool = True):
    T = TrapezoidalMap(segments)
    # q = randomPoint(T)
    # if flag: showMap(T, T.getTrapezoids(), T.segments,q,T.query(q).data)

size = [10,50,100,200,500,1000,2000,3000,4000,5000,10000]

def testTime(size: list[int]):
    table = []
    for i in size:
        S = generateSegment(i)
        start = time.time()
        test(S,False)
        end = time.time()
        table += [end - start]
        print("rozmiar: ",i,"czas: ",end - start)
    plt.scatter(size, table, color = 'green')
    plt.show()

testTime(size)