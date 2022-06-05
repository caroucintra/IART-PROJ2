import gym
from gym import spaces
import numpy as np
from gym_game.envs.gui import GUI



class Environment(gym.Env):


    def __init__(self):
        self.gui = GUI()
        self.game = self.gui.getGame()
        self.action_space = spaces.Discrete( len(self.game.getPossibleMoves()) )
        self.observation_space = self.game.calculatePossibleStates()

    
    def step(self, action):
        reward, state = self.gui.action(action)
        done = self.gui.done()
        return state, reward, done, {}

    
    def reset(self):
        del self.gui
        self.gui = GUI()
        state = self.gui.state()
        return state


    def render(self, mode='human', close=False):
        self.gui.view()


