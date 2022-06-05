from importlib.metadata import entry_points
from gym.envs.registration import register

register(
    id = 'Pygame-v0',
    entry_point = 'gym_game.envs:Environment',
    max_episode_steps = 2000,
)
