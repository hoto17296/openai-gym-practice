from gym.envs.registration import register
from .flappy import Flappy

register(
    id='Flappy-v0',
    entry_point='envs:Flappy',
)
