from abc import ABC, abstractmethod


class State(ABC):
    def __eq__(self, other):
        return hash(self) == hash(other)

    @abstractmethod
    def __str__(self): pass

    @abstractmethod
    def __hash__(self): pass
