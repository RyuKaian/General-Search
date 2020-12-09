class NodeSet:
    def __init__(self):
        self.set = set()

    def add(self, node):
        if node not in self.set:
            self.set.add(node)
            return True
        return False

    def __len__(self):
        return len(self.set)
