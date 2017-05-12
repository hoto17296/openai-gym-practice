import pyglet
from pyglet.gl import *
import gym
from gym import spaces
from gym.envs.classic_control.rendering import Transform, make_circle

class Flappy(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.window = pyglet.window.Window(width=480, height=640)
        self.actions = spaces.Discrete(2)
        self.circle_radius = 10

    def _step(self, action):
        assert self.actions.contains(action), "%r (%s) invalid"%(action, type(action))

        pos, accel = self.state

        if action:
            accel = 8
        else:
            accel -= 1
        pos += accel

        self.state = [pos, accel]

        reward = 1.0
        done = pos < self.circle_radius or pos > self.window.height
        info = {}

        return self.state, reward, done, info

    def _reset(self):
        self.state = [self.window.height - self.circle_radius, 0]
        return self.state

    def _render(self, mode='human', close=False):
        if close:
            self.window.close()
            return

        self.window.clear()
        self.window.switch_to()
        self.window.dispatch_events()

        self.render_background()

        pos, accel = self.state

        geom = make_circle(self.circle_radius)
        geom.add_attr(Transform(translation=(self.window.width/2, pos)))
        geom.render()

        self.window.flip()

    def render_background(self):
        glClearColor(1,1,1,1) # White

if __name__ == '__main__':
    from pyglet.window import key as KEY

    env = Flappy()

    action = False

    def key_press(key, mod):
        global action
        if key == KEY.SPACE:
            action = True

    def key_release(key, mod):
        global action
        if key == KEY.SPACE:
            action = False

    env.unwrapped.window.on_key_press = key_press
    env.unwrapped.window.on_key_release = key_release

    while True:
        observation = env.reset()
        done = False
        while not done:
            env.render()
            print(observation, action)
            observation, reward, done, info = env.step(action)
