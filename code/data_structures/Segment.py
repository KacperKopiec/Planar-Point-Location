from data_structures.Point import Point

class Segment:
    def __init__(self, p1, p2):
        if p1 > p2: p1, p2 = p2, p1
        self.left = p1
        self.right = p2

    def __det(self, a, b, c):
        return a[0] * b[1] + a[1] * c[0] + b[0] * c[1] - b[1] * c[0] - a[0] * c[1] - a[1] * b[0]

    def point_over_segment(self, p: Point, eps = 1e-8):
        """
        Determines the relative position of a point with respect to the segment.

        Parameters:
        - p (Point): The point to classify.
        - eps (float): Tolerance for collinearity.

        Returns:
        - int: 1 if the point is above, -1 if below, and 0 if on the segment.
        """
        d = self.__det([self.left.x, self.left.y], [self.right.x, self.right.y], [p.x, p.y])
        if d > eps: return 1
        if d < -eps: return -1
        return 0

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __hash__(self):
        return hash((self.left, self.right))
    
    def __str__(self):
        return f"({self.left},{self.right})"