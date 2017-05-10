import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym.envs.classic_control import rendering

class Flappy(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.state = None
        self.viewer = None
        self.action_space = spaces.Discrete(2)
        self.screen_width = 400
        self.screen_height = 600
        self.threshold = 0
        self.circle_width = 10

    def _step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        pos, accel = self.state

        if action:
            accel = 8
        else:
            accel -= 1
        pos += accel

        self.state = [pos, accel]
        reward = 1.0
        done = pos < self.threshold or pos > (self.screen_height - self.threshold)
        info = {}

        return np.array(self.state), reward, done, info

    def _reset(self):
        self.state = [self.screen_height / 2, 0]
        return np.array(self.state)

    def _render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return

        pos, accel = self.state

        if self.viewer is None:
            self.viewer = rendering.Viewer(self.screen_width, self.screen_height)
            self.trans = rendering.Transform()
            self.circle = rendering.make_circle(self.circle_width)
            self.circle.set_color(.3, .3, 1.0)
            self.circle.add_attr(self.trans)
            self.viewer.add_geom(self.circle)

        self.trans.set_translation(self.screen_width / 2, pos)

        return self.viewer.render(return_rgb_array = mode=='rgb_array')
