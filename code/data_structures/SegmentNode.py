class SegmentNode:
    def __init__(self, segment):
        self.data = segment
        self.left = None
        self.right = None
    
    def getType(self):
        return 1
    
    def setLeft(self, node):
        if node.getType() == 2: node.partents.append(self)
        self.left = node
    
    def setRight(self, node):
        if node.getType() == 2: node.partents.append(self)
        self.right = node