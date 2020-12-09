class SearchProblem:
    def __init__(self, operators, initial_node, goal_test, path_cost, heuristic):
        self.operators = operators
        self.initial_node = initial_node
        self.goal_test = goal_test
        self.path_cost = path_cost
        self.heuristic = heuristic
