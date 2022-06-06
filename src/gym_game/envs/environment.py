import gym
from gym import spaces
import numpy as np
from gym_game.envs.gui import GUI



class Environment(gym.Env):
    def __init__(self, **kwargs):
        self.size = kwargs['size']
        self.pieces = kwargs['pieces']
        self.snake = kwargs['snake']
        self.gui = GUI(self.size, self.snake, self.pieces)
        self.game = self.gui.getGame()
        self.action_space = spaces.Discrete( len(self.game.getPossibleMoves()) )
        self.observation_space = self.game.calculatePossibleStates()

    
    def step(self, action):
        reward, state, done = self.gui.action(action)
        return state, reward, done, {}

    
    def reset(self):
        del self.gui
        self.gui = GUI(self.size, self.snake, self.pieces)
        state = self.gui.state()
        print("STATE ", state)
        return state


    def render(self, mode='human', close=False):
        self.gui.view()

