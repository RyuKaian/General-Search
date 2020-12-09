from abc import ABC, abstractmethod

from GenericSearch.Helpers import NodeQueue, NodeSet


class Search(ABC):
    def __init__(self, problem, qing_func):
        self.problem = problem
        self.qing_func = qing_func

    def search(self):
        total_expanded = 0
        max_depth = -1

        while True:
            nodes = NodeQueue()
            max_depth += self.qing_func(nodes, [self.problem.initial_node])
            expanded_nodes = NodeSet()

            while nodes:
                node = nodes.dequeue()
                if expanded_nodes.add(node):
                    if self.problem.goal_test(node):
                        return node, total_expanded + len(expanded_nodes)
                    else:
                        self.qing_func(nodes, self.expand(node, max_depth))

            total_expanded += len(expanded_nodes)

    def expand(self, node, max_depth):
        if max_depth == -1 or node.depth <= max_depth:
            return [self.calculate_node_cost(child) for operator in self.problem.operators if (child := operator(node))]
        return []

    def calculate_node_cost(self, node):
        self.problem.path_cost(node)
        if self.problem.heuristic:
            self.problem.heuristic(node)
        return node

    @abstractmethod
    def operators(self): pass
