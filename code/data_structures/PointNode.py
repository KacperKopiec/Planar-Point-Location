class PointNode:
    def __init__(self, p):
        self.data = p
        self.left = None
        self.right = None
    
    def getType(self):
        return 0
    
    def setLeft(self, node):
        if node.getType() == 2: node.partents.append(self)
        self.left = node
    
    def setRight(self, node):
        if node.getType() == 2: node.partents.append(self)
        self.right = node