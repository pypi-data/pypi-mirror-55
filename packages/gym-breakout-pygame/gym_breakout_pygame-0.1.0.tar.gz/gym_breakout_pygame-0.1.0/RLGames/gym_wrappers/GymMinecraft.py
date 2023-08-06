from gym import Space
from gym.spaces import Discrete, Dict, Tuple

from RLGames.Minecraft import Minecraft
import RLGames.Minecraft as m
from RLGames.gym_wrappers.GymPygameWrapper import GymPygameWrapper

from RLGames.utils import DummyAgent, get_locals_no_self


class GymMinecraft(GymPygameWrapper, Minecraft):
    """Wrapper for the Breakout pygame"""

    PygameEnvClass = Minecraft

    def __init__(self, differential=False):
        GymPygameWrapper.__init__(self, **get_locals_no_self(locals()))
        Minecraft.__init__(self)
        self.differential = differential
        self.init(DummyAgent())

        # ntasks = 1
        # for t in list(m.TASKS.keys()):
        #     ntasks *= len(m.TASKS[t])+1

        d = {}
        for l, _, _, _ in m.LOCATIONS:
            d[l] = Discrete(2)


        self.observation_space = Dict({
            "x":          Discrete(self.cols),
            "y":          Discrete(self.rows),
            "theta":      Discrete(4),                   # four directions: North - South - East - West
            "location":   Discrete(len(m.LOCATIONS) + 1),
            "actionlocation": Dict(d)
        })
        self.action_space = Discrete(self.nactions)


    def getstate(self):
        d = {}
        for l, _, u, v in m.LOCATIONS:
            if (u, v) in self.actionlocation:
                d[l] = 1
            else:
                d[l] = 0

        return {
            "x":            self.pos_x,
            "y":            self.pos_y,
            "theta":        int(self.pos_th/90),
            "location":     self.get_item(),
            "actionlocation": d
        }


    def getreward(self):
        return 0

    def get_item(self):
        x, y = self.pos_x, self.pos_y
        for idx, t in enumerate(self.locations):
            if (t[2] == x and t[3] == y):
                return idx
        return len(self.locations)

    def step(self, action):
        obs, reward, done, info = super().step(action)
        if self.numactions > self.nactionlimit:
            # stop the game if too much actions
            done = True
        else:
            done = False

        # make always the goal true, the true goals are specified by temporal evaluators
        info["goal"] = True
        return obs, reward, done, info

    def goal_reached(self):
        return True