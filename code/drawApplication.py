import tkinter as tk
from data_structures.Point import Point
from data_structures.Segment import Segment

def draw():
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=800)
    canvas.pack()
    vertices = []
    new_vertices = []
    points = []
    lines = []
    new_lines = []
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
        point = Point(event.x, event.y)
        points += [point]
        canvas.create_oval(point.x - 2, point.y - 2, point.x + 2, point.y + 2, fill = "black", width = 1)
        canvas.create_line(points[-2].to_tuple(), points[-1].to_tuple(), fill="black",width = 4)
        lines += [Segment(points[-2],points[-1])]
    canvas.bind('<Button-1>', start_line)
    canvas.bind('<ButtonRelease-1>',end_line)
    
    def close_window():
        nonlocal lines
        nonlocal new_lines
        new_lines = [((seg.left.x,500-seg.left.y),(seg.right.x,500-seg.right.y)) for seg in lines]
        print(f"{new_lines}")
        root.quit()
        root.destroy() 
    close_button = tk.Button(root, text="Zakończ", command=close_window)
    close_button.pack(pady=20)
    canvas.mainloop()
    return new_lines

draw()