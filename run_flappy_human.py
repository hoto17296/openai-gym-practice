import gym
import envs

env = gym.make('Flappy-v0')

action = False

def key_press(key, mod):
    global action
    if key == 32:
        action = True

def key_release(key, mod):
    global action
    if key == 32:
        action = False

for episode in range(10):
    observation = env.reset()
    done = False
    while not done:
        env.render()
        env.unwrapped.viewer.window.on_key_press = key_press
        env.unwrapped.viewer.window.on_key_release = key_release
        print(observation, action)
        observation, reward, done, info = env.step(action)
