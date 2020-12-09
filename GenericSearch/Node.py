from abc import ABC


class Node(ABC):
    def __init__(self, state, parent=None, operator=None, depth=0, path_cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.operator = operator
        self.depth = depth
        self.path_cost = path_cost
        self.heuristic = heuristic

    def __eq__(self, other):
        return self.state == other.state

    def __str__(self):
        return f'Operator: {self.operator}, State: ({self.state}), Depth: {self.depth},' \
               f' Cost: {self.path_cost}, Heuristic: {self.heuristic}'

    def __hash__(self):
        return hash(self.state)

    def lt_gh(self, other):
        return (self.path_cost + self.heuristic) < (other.path_cost + other.heuristic)

    def lt_h(self, other):
        return self.heuristic < other.heuristic

    def get_all_operators(self):
        output = ''
        if self.parent:
            output += self.parent.get_all_operators()
            output += (',' if output else '') + self.operator
        return output
