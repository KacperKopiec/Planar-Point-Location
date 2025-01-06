import tkinter as tk
from data_structures.Point import Point
from data_structures.Segment import Segment
from data_structures.TrapezoidalMap import *

def draw():
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=800)
    canvas.pack()
    vertices = []
    new_vertices = []
    points = []
    lines = []
    new_lines = []
    is_drawing_point =False
    q = None
    def start_line(event):
        nonlocal vertices
        nonlocal points
        point = Point(event.x, event.y)
        points += [point]
        canvas.create_oval(point.x - 2, point.y - 2, point.x + 2, point.y + 2, fill = "black", width = 1)
    def end_line(event):
        nonlocal vertices
        nonlocal new_vertices
        nonlocal points
        nonlocal lines
        nonlocal q
        nonlocal is_drawing_point
        if is_drawing_point:
            # If in point-drawing mode, draw the single point
            q = Point(event.x, event.y)
            canvas.create_oval(
                q.x - 4, q.y - 4, q.x + 4, q.y + 4, fill="red", width=1
            )
            q.y = 500 - q.y
            is_drawing_point = False
        else:
            point = Point(event.x, event.y)
            points += [point]
            canvas.create_oval(point.x - 2, point.y - 2, point.x + 2, point.y + 2, fill = "black", width = 1)
            canvas.create_line(points[-2].to_tuple(), points[-1].to_tuple(), fill="black",width = 4)
            lines += [Segment(points[-2],points[-1])]
    canvas.bind('<Button-1>', start_line)
    canvas.bind('<ButtonRelease-1>',end_line)
    
    def add_point():
        nonlocal is_drawing_point
        is_drawing_point = True
    def close_window():
        nonlocal lines
        nonlocal new_lines
        new_lines = [Segment(Point(seg.left.x,500-seg.left.y),Point(seg.right.x,500-seg.right.y)) for seg in lines]
        # print("segments = [")
        # for a, b in new_lines:
        #     print(f"    Segment(Point{a}, Point{b}),")
        # print("]")
        root.quit()
        root.destroy() 
    close = tk.Button(root, text= "Koniec odcinków", command = add_point)
    close.pack(pady = 20)
    close_button = tk.Button(root, text="Zakończ", command=close_window)
    close_button.pack(pady=20)
    canvas.mainloop()
    return new_lines,q




