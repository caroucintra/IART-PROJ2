import sys
import numpy as np
import math
import random
import time
from gym_game.envs.environment import Environment


import gym
import gym_game

def simulate():
    global epsilon, epsilon_decay
    for episode in range(MAX_EPISODES):

        # Init environment
        state = env.reset()
        total_reward = 0

        # AI tries up to MAX_TRY times
        for t in range(MAX_TRY):

            # In the beginning, do random action to learn
            if random.uniform(0, 1) < epsilon:
                action = env.action_space.sample()
            else:
                action = np.argmax(q_table[state])

            # Do action and get result
            next_state, reward, done, _ = env.step(action)
            total_reward += reward

            # Get correspond q value from state, action pair
            q_value = q_table[state][action]
            best_q = np.max(q_table[next_state])
            
            
            q_table[state, action] = q_table[state, action] + learning_rate * (reward + gamma * np.max(q_table[next_state, :]) - q_table[state, action])


            # Q(state, action) <- (1 - a)Q(state, action) + a(reward + rmaxQ(next state, all actions))
            #q_table[state][action] = (1 - learning_rate) * q_value + learning_rate * (reward + gamma * best_q)

            # Set up for the next iteration
            state = next_state

            # Draw games
            #env.render()

            # When episode is done, print reward
            if done or t >= MAX_TRY - 1:
                print("Episode %d finished after %i time steps with total reward = %f." % (episode, t, total_reward))
                break

        # exploring rate decay
        if epsilon >= 0.005:
            epsilon *= epsilon_decay
    print(q_table)

def choose_random_puzzle():
    puzzles = {
        "puzzle1":  
    }


if __name__ == "__main__":
    puzzle_size, puzzle_snake, puzzle_pieces = choose_random_puzzle()
    env = gym.make("Pygame-v0", size = 4, snake = [[0,3],[0,2], [1, 2], [2,2], [2,1], [2,0],[3,0]], pieces = ['H','H','H'])

    MAX_EPISODES = 40000
    MAX_TRY = 1000
    epsilon = 1
    epsilon_decay = 0.9999
    learning_rate = 0.9
    gamma = 0.5
    action_size = env.action_space.n
    state_size = env.observation_space
    print(f'action size: {action_size}, state size: {state_size}')
    q_table = np.zeros((state_size, action
    _size))
    simulate()
    env.reset()

    for episode in range(5):
        state = env.reset()
        step = 0
        done = False
        print("****************************************************")
        print("EPISODE ", episode)

        for step in range(50):
            #env.render()
            
            # Take the action (index) that have the maximum expected future reward given that state
            action = np.argmax(q_table[state,:])
            
            new_state, reward, done, info = env.step(action)
            state = new_state

            
            if done:
                break
        #time.sleep(5)

    env.render()
    env.close()
