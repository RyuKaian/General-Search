from GenericSearch import Node


class MINode(Node):
    @property
    def position(self):
        return self.state.position

    @property
    def carrying(self):
        return self.state.carrying

    @property
    def remaining_imf(self):
        return self.state.remaining_imf
