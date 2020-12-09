from abc import ABC, abstractmethod


class QingFunction(ABC):
    @staticmethod
    @abstractmethod
    def queue(nodes, expanded_nodes): pass


class BFS(QingFunction):
    @staticmethod
    def queue(nodes, expanded_nodes):
        for node in expanded_nodes:
            nodes.append(node)
        return 0


class DFS(QingFunction):
    @staticmethod
    def queue(nodes, expanded_nodes):
        expanded_nodes.reverse()
        for node in expanded_nodes:
            nodes.prepend(node)
        return 0


class UCS(QingFunction):
    @staticmethod
    def queue(nodes, expanded_nodes):
        for node in expanded_nodes:
            nodes.ordered_insert_gh(node)
        return 0


class IDS(QingFunction):
    @staticmethod
    def queue(nodes, expanded_nodes):
        DFS.queue(nodes, expanded_nodes)
        return 1


class GRS(QingFunction):
    @staticmethod
    def queue(nodes, expanded_nodes):
        for node in expanded_nodes:
            nodes.ordered_insert_h(node)
        return 0


class ASS(QingFunction):
    @staticmethod
    def queue(nodes, expanded_nodes):
        return UCS.queue(nodes, expanded_nodes)
