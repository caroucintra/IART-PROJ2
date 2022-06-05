import gym
from gym import spaces
import numpy as np
from gym_game.envs.gui import GUI



class Environment(gym.Env):


    def __init__(self):
        pieces = ['Q', 'Q','Q']
        self.gui = GUI(4, [[0,3],[0,2], [1, 2], [2,2], [2,1], [2,0],[3,0]], pieces)
        self.game = self.gui.getGame()
        self.action_space = spaces.Discrete( len(self.game.getPossibleMoves()) )
        self.observation_space = self.game.calculatePossibleStates()

    
    def step(self, action):
        reward, state, done = self.gui.action(action)
        return state, reward, done, {}

    
    def reset(self):
        pieces = ['H', 'H','H']
        del self.gui
        self.gui = GUI(4, [[0,3],[0,2], [1, 2], [2,2], [2,1], [2,0],[3,0]], pieces)
        state = self.gui.state()
        print("STATE ", state)
        return state


    def render(self, mode='human', close=False):
        self.gui.view()


