import gym
from gym import spaces
import numpy as np
from gui import GUI


class Environment(gym.Env):


    def __init__(self, game):
        self.gui = GUI()
        self.action_space = spaces.Discrete(4)

        self._action_to_direction = {
            0: np.array([1, 0]),
            1: np.array([0, 1]),
            2: np.array([-1, 0]),
            3: np.array([0, -1]),
        }
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(0, game.getSize() - 1, shape=(2,), dtype=int),
                "target": spaces.Box(0, game.getSize() - 1, shape=(2,), dtype=int),
            }
        )

    
    def step(self, action):
        self.gui.action(action)
        state = self.gui.state()
        reward = self.gui.reward()
        done = self.gui.done()
        return state, reward, done, {}

    
    def reset(self):
        del self.gui
        self.gui = GUI()
        state = self.gui.state()
        return state


    def render(self, mode='human', close=False):
        self.gui.view()


