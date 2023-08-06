import os
import sys

import numpy as np
from gym import Env
from gym.spaces import Discrete, Box, Dict

from RLGames import Breakout as b
from RLGames.Breakout import Breakout
from RLGames.gym_wrappers.GymPygameWrapper import GymPygameWrapper
from RLGames.utils import DummyAgent, get_locals_no_self


class GymBreakout(GymPygameWrapper, Breakout):
    """Wrapper for the Breakout pygame"""

    PygameEnvClass = Breakout

    def __init__(self, brick_rows=3, brick_cols=3, trainsessionname='test', deterministic=True):
        GymPygameWrapper.__init__(self, **get_locals_no_self(locals()))
        Breakout.__init__(self, brick_rows, brick_cols, trainsessionname=trainsessionname)
        self.deterministic = deterministic
        self.sound_enabled = False
        self.init(DummyAgent())

        self.observation_space = Dict({
            "ball_x": Discrete(self.n_ball_x),
            "ball_y": Discrete(self.n_ball_y),
            "ball_dir": Discrete(self.n_ball_dir),
            "paddle_x": Discrete(self.n_paddle_x),
            "diff_paddle_ball": Discrete(self.n_diff_paddle_ball),
            "bricks_matrix": Box(low=0, high=1, shape=(self.brick_cols, self.brick_rows), dtype=np.uint8)
        })

        self.action_space = Discrete(self.nactions)

    def getstate(self):
        resx = b.resolutionx  # highest resolution
        resy = b.resolutiony  # highest resolution
        if (self.ball_y < self.win_height // 3):  # upper part, lower resolution
            resx *= 3
            resy *= 3
        elif (self.ball_y < 2 * self.win_height // 3):  # lower part, medium resolution
            resx *= 2
            resy *= 2

        ball_x = int(self.ball_x) // resx
        ball_y = int(self.ball_y) // resy
        ball_dir = 0
        if self.ball_speed_y > 0:  # down
            ball_dir += 5
        if self.ball_speed_x < -2.5:  # quick-left
            ball_dir += 1
        elif self.ball_speed_x < 0:  # left
            ball_dir += 2
        elif self.ball_speed_x > 2.5:  # quick-right
            ball_dir += 3
        elif self.ball_speed_x > 0:  # right
            ball_dir += 4

        if self.simple_state:
            paddle_x = 0
        else:
            paddle_x = int(self.paddle_x) // resx

        diff_paddle_ball = int((self.ball_x - self.paddle_x + self.win_width) / b.resolutionx)

        return {
            "ball_x":   ball_x,
            "ball_y":   ball_y,
            "ball_dir": ball_dir,
            "paddle_x": paddle_x,
            "diff_paddle_ball": diff_paddle_ball,
            "bricks_matrix": self.bricksgrid
        }


    def setStateActionSpace(self):
        self.n_ball_x = int(self.win_width / b.resolutionx) + 1
        self.n_ball_y = int(self.win_height / b.resolutiony) + 1
        self.n_ball_dir = 10  # ball going up (0-5) or down (6-9)
        # ball going left (1,2) straight (0) right (3,4)
        self.n_paddle_x = int(self.win_width / b.resolutionx) + 1

        self.nactions = 3  # 0: not moving, 1: left, 2: right
        if (self.fire_enabled):
            self.nactions = 4  # 3: fire

        self.n_diff_paddle_ball = int(2*self.win_width/b.resolutionx)+1
        self.nstates = None




