import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym.envs.classic_control import rendering
import Box2D
from Box2D.b2 import edgeShape, circleShape, fixtureDef, polygonShape, revoluteJointDef, contactListener

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

        self.world = Box2D.b2World(gravity=(0, -10))
        self.ground = self.world.CreateStaticBody(position=(0, 1), shapes=polygonShape(box=(self.screen_width, 5)))
        self.circle = self.world.CreateDynamicBody(position=(200, 400), shapes=circleShape(radius=self.circle_width/2))

        self.circle.ApplyForceToCenter((0, -1000.0), True)

        self.ground.color1 = (0.5, 0.4, 0.9)
        self.ground.color2 = (0.3, 0.3, 0.5)
        self.circle.color1 = (0.5, 0.4, 0.9)
        self.circle.color2 = (0.3, 0.3, 0.5)

    def _step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        pos, accel = self.state

        if action:
            accel = 8
            self.circle.ApplyLinearImpulse(impulse=(0,2), point=(0,0), wake=True)
        else:
            accel -= 1
        pos += accel

        self.state = [pos, accel]
        reward = 1.0
        #done = pos < self.threshold or pos > (self.screen_height - self.threshold)
        done = pos > (self.screen_height - self.threshold)
        info = {}

        timeStep = 1.0 / 60
        vel_iters, pos_iters = 6*30, 2*30
        self.world.Step(timeStep, vel_iters, pos_iters)

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

        if self.viewer is None:
            self.viewer = rendering.Viewer(self.screen_width, self.screen_height)

        self.draw_obj(self.ground)
        self.draw_obj(self.circle)

        return self.viewer.render(return_rgb_array = mode=='rgb_array')

    def draw_obj(self, obj):
        for f in obj.fixtures:
            trans = f.body.transform
            if type(f.shape) is circleShape:
                t = rendering.Transform(translation=trans * f.shape.pos)
                self.viewer.draw_circle(f.shape.radius, 20, color=obj.color1).add_attr(t)
                self.viewer.draw_circle(f.shape.radius, 20, color=obj.color2, filled=False, linewidth=2).add_attr(t)
            else:
                path = [trans * v for v in f.shape.vertices]
                self.viewer.draw_polygon(path, color=obj.color1)
                path.append(path[0])
                self.viewer.draw_polyline(path, color=obj.color2, linewidth=2)