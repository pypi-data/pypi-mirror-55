from gym.spaces import Discrete, Dict

from RLGames.SimpleGrid import SimpleGrid
from RLGames.gym_wrappers.GymPygameWrapper import GymPygameWrapper
from RLGames.utils import DummyAgent, get_locals_no_self


class GymSimpleGrid(GymPygameWrapper, SimpleGrid):
    """Wrapper for the Breakout pygame"""

    PygameEnvClass = SimpleGrid

    def __init__(self, rows=3, cols=3, trainsessionname='test'):
        GymPygameWrapper.__init__(self, **get_locals_no_self(locals()))
        SimpleGrid.__init__(self, rows, cols, trainsessionname=trainsessionname)
        self.init(DummyAgent())

        self.observation_space = Dict({
            "x": Discrete(self.rows),
            "y": Discrete(self.cols),
        })

        self.action_space = Discrete(self.nactions)

    def getstate(self):
        return {
            "x": self.pos_x,
            "y": self.pos_y,
        }
