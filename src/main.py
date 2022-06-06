import sys
import numpy as np
import math
import random
import time
import matplotlib.pyplot as plt
import numpy as np

from gym_game.envs.environment import Environment


import gym

def simulateSARSA():
    global epsilon, epsilon_decay


    for episode in range(MAX_EPISODES):
        # Init environment
        state = env.reset()
        total_reward = 0
        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(q_table[state])

        # AI tries up to MAX_TRY times
        for t in range(MAX_TRY):

            # In the beginning, do random action to learn
            
            # Do action and get result
            next_state, reward, done, _ = env.step(action)
            print(next_state, reward, done)
            total_reward += reward

            # Get correspond q value from state, action pair
            q_value = q_table[state][action]

            if random.uniform(0, 1) < epsilon:
                new_action = env.action_space.sample()
            else:
                new_action = np.argmax(q_table[next_state])

            best_q = q_table[next_state][new_action]
            
            q_table[state, action] = q_value + learning_rate * (reward + gamma * best_q) - q_value
            # Set up for the next iteration
            state = next_state
            action = new_action

            # Draw games
            #env.render()

            # When episode is done, print reward
            if done or t >= MAX_TRY - 1:
                print("Episode %d finished after %i time steps with total reward = %f." % (episode, t, total_reward))
                break

        # exploring rate decay
        if epsilon >= 0.005:
            epsilon *= epsilon_decay

        ep_rewards.append(total_reward)
        if(episode % 500 == 0):
            average_reward = sum(ep_rewards[-500:])/500
            aggr_ep_rewards['ep'].append(episode)
            aggr_ep_rewards['avg'].append(average_reward)
            aggr_ep_rewards['max'].append(max(ep_rewards[-500:]))
            aggr_ep_rewards['min'].append(min(ep_rewards[-500:]))
            print(f'Episode: {episode:>5d}, average reward: {average_reward:>4.1f}, current epsilon: {epsilon:>1.2f}')


    print(q_table)


def simulateQLearning( ):
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
            #action = 8
            next_state, reward, done, _ = env.step(action)
            total_reward += reward

            # Get correspond q value from state, action pair
            q_value = q_table[state][action]

            best_q = np.max(q_table[next_state, :])
            
            q_table[state, action] = q_value + learning_rate * (reward + gamma * best_q) - q_table[state, action]

            # Set up for the next iteration
            state = next_state

            # Draw games
            #env.render()
                

            # When episode is done, print reward
            if done or t >= MAX_TRY - 1:
                print("Episode %d finished after %i time steps with total reward = %f." % (episode, t, total_reward))
                break

        ep_rewards.append(total_reward)

        if(episode % 500 == 0):
            average_reward = sum(ep_rewards[-500:])/500
            aggr_ep_rewards['ep'].append(episode)
            aggr_ep_rewards['avg'].append(average_reward)
            aggr_ep_rewards['max'].append(max(ep_rewards[-500:]))
            aggr_ep_rewards['min'].append(min(ep_rewards[-500:]))
            print(f'Episode: {episode:>5d}, average reward: {average_reward:>4.1f}, current epsilon: {epsilon:>1.2f}')


        # exploring rate decay
        if epsilon >= 0.005:
            epsilon *= epsilon_decay
    print(q_table)
   


def choose_random_puzzle():
    puzzles = {
        "puzzle1": [4, [[0,3],[0,2], [1, 2], [2,2], [2,1], [2,0],[3,0]], ['Q','Q','Q']],
        "puzzle2": [3, [[0,2], [1, 2], [2,2], [2,1], [2,0]], ['B', 'T']],
        "puzzle3": [4, [[0,3],[0,2], [1, 2], [2,2], [2,1], [2,0],[3,0]], ['H','B']],
        "puzzle4": [3, [[0,2], [0,1], [1,1], [2,1], [2,0]], ['Q','Q']],
        "puzzle5": [5, [[0,4], [ 1,4], [ 1,3], [2,3], [ 2, 2], [ 3,2], [3,1],[3,0],[4,0]], ['T','Q','T']],
    }

    return puzzles['puzzle5'][0], puzzles['puzzle5'][1], puzzles['puzzle5'][2] 


if __name__ == "__main__":
    puzzle_size, puzzle_snake, puzzle_pieces = choose_random_puzzle()
    env = gym.make("Pygame-v0", size = puzzle_size, snake = puzzle_snake, pieces = puzzle_pieces)

    MAX_EPISODES = 10000
    MAX_TRY = 10
    epsilon = 1
    epsilon_decay = 0.9999
    learning_rate = 0.8
    gamma = 0.5
    ep_rewards = []
    aggr_ep_rewards = {'ep': [], 'avg': [], 'max': [], 'min': []}
    action_size = env.action_space.n
    state_size = env.observation_space
    print(f'action size: {action_size}, state size: {state_size}')
    q_table = np.zeros((state_size, action_size))
    simulateQLearning()
    plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['avg'], label="average rewards")
    plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['max'], label="max rewards")
    plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['min'], label="min rewards")
    plt.legend(loc=4)
    plt.show()

    
    state = env.reset()

    done =False

    while(not done):
        # Take the action (index) that have the maximum expected future reward given that state
        action = np.argmax(q_table[state,:])
        
        new_state, reward, done, info = env.step(action)
        state = new_state
        print(reward)
        env.render()

    env.render()
    
    env.close()
