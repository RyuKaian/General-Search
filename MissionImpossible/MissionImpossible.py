import math

from GenericSearch import ASS, BFS, DFS, GRS, IDS, Search, SearchProblem, UCS
from MissionImpossible.MINode import MINode
from MissionImpossible.MIState import MIState


class MissionImpossible(Search):
    def __init__(self, grid, strategy, visualize):
        self.map = self.Map(grid)
        if visualize:
            print(self.map)

        initial_node = MINode(MIState(self.map.ethan, 0, self.map.imf_agents))

        qing_func, heuristic = self.qing_func(strategy)

        problem = SearchProblem(self.operators(), initial_node, self.goal_test, self.path_cost, heuristic)
        super().__init__(problem, qing_func)

    def search(self):
        try:
            solution, expanded_nodes_count = super(MissionImpossible, self).search()

            if solution:
                print(solution)
                return f'{solution.get_all_operators()};'\
                       f'{solution.remaining_imf.deaths};'\
                       f'{",".join([str(imf) for imf in solution.remaining_imf])};'\
                       f'{expanded_nodes_count}'
        except TypeError:
            return 'No Solution found'

    def qing_func(self, strategy):
        qing_funcs = {'BF': BFS, 'DF': DFS, 'UC': UCS, 'ID': IDS, 'GR1': GRS, 'GR2': GRS, 'AS1': ASS, 'AS2': ASS}
        qing_func = qing_funcs.get(strategy, None)

        heuristic = self.heuristic1 if '1' in strategy else self.heuristic2 if '2' in strategy else None

        return qing_func.queue, heuristic

    @staticmethod
    def goal_test(node):
        return node.operator == 'drop' and len(node.remaining_imf) == 0

    @staticmethod
    def path_cost(node):
        damage = node.remaining_imf.damage(2)
        if node.operator not in ['drop', 'carry']:
            node.path_cost += damage + 1

    @staticmethod
    def distance_from_sub(ethan: tuple, sub: tuple):
        return math.sqrt((ethan[0] - sub[0]) ** 2 + (ethan[1] - sub[1]) ** 2)

    def heuristic1(self, node):
        node.heuristic = len(node.remaining_imf) + self.distance_from_sub(node.position, self.map.sub)

    def heuristic2(self, node):
        for imf in node.remaining_imf:
            if imf.hp == 100 and imf.not_safe:
                node.heuristic += 10000
        # node.heuristic = len(node.remaining_imf)
        node.heuristic += self.distance_from_sub(node.position, self.map.sub)

    def operators(self):
        def up(node):
            new_pos = (node.position[0] - 1, node.position[1])
            if 0 <= new_pos[0] < self.map.width and 0 <= new_pos[1] < self.map.height:
                return MINode(MIState(new_pos, node.carrying, node.remaining_imf.clone()), node, 'up', node.depth + 1,
                              node.path_cost)

        def down(node):
            new_pos = (node.position[0] + 1, node.position[1])
            if 0 <= new_pos[0] < self.map.width and 0 <= new_pos[1] < self.map.height:
                return MINode(MIState(new_pos, node.carrying, node.remaining_imf.clone()), node, 'down', node.depth + 1,
                              node.path_cost)

        def left(node):
            new_pos = (node.position[0], node.position[1] - 1)
            if 0 <= new_pos[0] < self.map.width and 0 <= new_pos[1] < self.map.height:
                return MINode(MIState(new_pos, node.carrying, node.remaining_imf.clone()), node, 'left', node.depth + 1,
                              node.path_cost)

        def right(node):
            new_pos = (node.position[0], node.position[1] + 1)
            if 0 <= new_pos[0] < self.map.width and 0 <= new_pos[1] < self.map.height:
                return MINode(MIState(new_pos, node.carrying, node.remaining_imf.clone()), node, 'right',
                              node.depth + 1, node.path_cost)

        def carry(node):
            if self.map.get(
                    node.position) == 'f' and node.carrying < self.map.carry_capacity and node.position in node.remaining_imf:
                remaining_imf = node.remaining_imf.clone()
                remaining_imf.remove(node.position)
                return MINode(MIState(node.position, node.carrying + 1, remaining_imf), node, 'carry', node.depth + 1,
                              node.path_cost)

        def drop(node):
            if self.map.get(node.position) == 's' and node.carrying != 0:
                return MINode(MIState(node.position, 0, node.remaining_imf.clone()), node, 'drop', node.depth + 1,
                              node.path_cost)

        return [drop, carry, up, left, down, right]

    class Map:
        def __init__(self, grid):
            self.grid = grid
            grid_elements = grid.split(';')

            self.width, self.height = self._int_split(grid_elements[0])
            self.map = [['-' for _ in range(self.height)] for _ in range(self.width)]

            self.ethan = self._int_split(grid_elements[1])
            self.set(self.ethan, 'e')

            self.sub = self._int_split(grid_elements[2])
            self.set(self.sub, 's')

            imfs = self._int_split(grid_elements[3])
            imfs_hp = self._int_split(grid_elements[4])

            self.imf_agents = self.IMFAgentList(
                [self.IMFAgent((imfs[(j := 2 * i)], imfs[j + 1]), hp) for i, hp in enumerate(imfs_hp)])
            for imf in self.imf_agents:
                self.set(imf.position, 'f')

            self.carry_capacity = int(grid_elements[5])

        @staticmethod
        def _int_split(string):
            return tuple([int(element) for element in string.split(',')])

        def __str__(self):
            return f'{self.grid}\n' + '\n'.join([' '.join(row) for row in self.map])

        def get(self, item):
            return self.map[item[0]][item[1]]

        def set(self, key, value):
            self.map[key[0]][key[1]] = value

        class IMFAgent:
            def __init__(self, position, hp, state='hurt'):
                self.position = position
                self.hp = hp
                self.state = state

            def __eq__(self, other):
                return self.position == other

            def __str__(self):
                return f'{self.hp}{self.position}'

            def __hash__(self):
                return hash(self.position)

            def clone(self):
                return self.__class__((self.position[0], self.position[1]), self.hp, self.state)

            def damage(self, damage_amount):
                if self.hp < 100:
                    self.hp += damage_amount
                    if self.hp > 100:
                        self.hp = 100
                return damage_amount

            def save(self):
                self.state = 'safe'
                return self

            def not_safe(self):
                return self.state == 'hurt'

        class IMFAgentList:
            def __init__(self, imfs):
                self.imfs = imfs

            def __str__(self):
                return f"[{', '.join([str(imf) for imf in self.imfs if imf.not_safe()])}]"

            def __len__(self):
                return len([imf for imf in self.imfs if imf.not_safe()])

            def __contains__(self, item):
                if item in self.imfs:
                    return self.imfs[self.imfs.index(item)].not_safe()

            def __hash__(self):
                total = 0
                for imf in self.imfs:
                    if imf.not_safe():
                        total += hash(imf)
                return total

            def __getitem__(self, item):
                return self.imfs[item]

            def clone(self):
                return self.__class__([imf.clone() for imf in self.imfs])

            def remove(self, imf_coord):
                self.imfs[self.imfs.index(imf_coord)].save()

            @property
            def deaths(self):
                deaths = 0
                for imf in self.imfs:
                    if imf.hp == 100:
                        deaths += 1
                return deaths

            def damage(self, damage_amount):
                total_damage = 0
                for imf in self.imfs:
                    if imf.not_safe():
                        total_damage += imf.damage(damage_amount)
                return total_damage
