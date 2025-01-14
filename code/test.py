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
def changeToSegments(lista: list[tuple]):
    segments = []
    for a,b in lista:
        segments+=[Segment(Point(a[0],a[1]),Point(b[0],b[1]))]
    return segments

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

size = [10,50,200,400,700,1000,3000,5000,8000,10000,15000,20000,30000,50000,75000,100000]

def testTime(size: list[int]):
    buld = []
    search = []
    for i in size:
        suma_czas = 0
        suma_ilosc = 0
        for j in range(10):
            S = generateSegment(i)
            start = time.time()
            T = TrapezoidalMap(S)
            end = time.time()
            suma_czas += end - start
            punkty = randomPoint(T, 1000)
            start = time.time()
            for q in punkty:
                T.query(q).data
            end = time.time()
            suma_ilosc += end - start
        print("n",i,"kosntrukcja: ",suma_czas/10,"wyszukanie: ",suma_ilosc)
        search += [suma_ilosc/10]
        buld += [suma_czas/10]
    
    z_b = np.polyfit(size, buld, 1)
    p_b = np.poly1d(z_b)
    plt.plot(size, p_b(size))
    plt.scatter(size, buld, color = 'green')
    plt.show()
    z_s = np.polyfit(size, search, 4)
    p_s = np.poly1d(z_s)
    plt.plot(size, p_s(size))
    plt.scatter(size, search, color = 'blue')
    plt.show()