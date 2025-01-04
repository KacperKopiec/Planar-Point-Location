class TrapezoidNode:
    def __init__(self, trapezoid):
        self.data = trapezoid
        self.parents = []
    
    def getType(self):
        return 2
    
    def replace(self, node):
        for parent in self.parents:
            if parent.left == self:
                parent.left = node
            else:
                parent.right = node