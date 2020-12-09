class NodeQueue:
    def __init__(self):
        self.queue = []

    def __bool__(self):
        return len(self.queue) != 0

    def dequeue(self):
        return self.queue.pop(0)

    def append(self, node):
        self.queue.append(node)

    def prepend(self, node):
        self.queue.insert(0, node)

    def ordered_insert_gh(self, node):
        if not len(self.queue) or not node.lt_gh(self.queue[-1]):
            return self.queue.append(node)

        for i, inode in enumerate(self.queue):
            if node.lt_gh(inode):
                return self.queue.insert(i, node)

    def ordered_insert_h(self, node):
        if not len(self.queue) or not node.lt_h(self.queue[-1]):
            return self.queue.append(node)

        for i, inode in enumerate(self.queue):
            if node.lt_h(inode):
                return self.queue.insert(i, node)
