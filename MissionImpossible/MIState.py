from GenericSearch import State


class MIState(State):
    def __init__(self, position, carrying, remaining_imf):
        self.position = position
        self.carrying = carrying
        self.remaining_imf = remaining_imf

    def __str__(self):
        return f'Location: {self.position}, Carrying: {self.carrying}, Remaining IMF: {self.remaining_imf}'

    def __hash__(self):
        return -hash(self.position) + hash(self.carrying) + hash(self.remaining_imf)
