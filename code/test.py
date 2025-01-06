import numpy as np
from examples import *
from visualisation import *
from data_structures.TrapezoidalMap import *
import time

def randomPoint(mapa : TrapezoidalMap, n: int = 1):
    trapez = mapa.createBoundary()
    A,B,C,D = trapez.trapezoidBoundary()
    punkty = []
    for _ in range(n):
        punkty.append(Point(np.random.uniform(A.x,D.x),np.random.uniform(A.y,B.y)))
    return punkty

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

size = [10,200,400,700,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,15000,20000,40000,60000,80000,100000]

def testTime(size: list[int]):
    buld = []
    search = []
    for i in size:
        S = generateSegment(i)
        start = time.time()
        T = TrapezoidalMap(S)
        end = time.time()
        buld += [end - start]
        print("rozmiar: ",i,"czas: ",end - start)
        punkty = randomPoint(T, i)
        start = time.time()
        for q in punkty:
            T.query(q).data
        end = time.time()
        search += [end - start]
        print("rozmiar: ",i,"czas: ",end - start)
    z_b = np.polyfit(size, buld, 1)
    p_b = np.poly1d(z_b)
    plt.title("Zależność czasu od liczby odcinków oraz od liczby wyszukiwań")
    plt.xlabel("Liczba odcinków S i wyszukiwań")
    plt.ylabel("sekundy")
    # plt.plot(size, p_b(size))
    # plt.scatter(size, buld, color = 'green')
    z_s = np.polyfit(size, search, 1)
    p_s = np.poly1d(z_s)
    plt.plot(size, p_s(size))
    plt.scatter(size, search, color = 'blue')
    plt.show()

testTime(size)
