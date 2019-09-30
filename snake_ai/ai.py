import random
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
from keras.layers.core import Dense, Dropout
from keras.models import Sequential
from keras.optimizers import Adam


class Agent(ABC):
    """Interface for all snake-playing deep learning agents."""
    @abstractmethod
    def make_choice(self, game_state):
        """Determines a choice based on internal state and the given game state.

        :returns an integer 0-3 corresponding to a directional input UP, DOWN, LEFT, or RIGHT."""
        pass

    @abstractmethod
    def set_reward(self, reward):
        """Reward or punish the agent for the resulting decision.

        :param reward an integer representing the reward for an action. Negative values are considered punishments.
            Larger magnitudes correspond to more strongly weighted rewards."""
        pass

    @abstractmethod
    def dump_weights(self):
        """Output a list of weights that affect the decision making process."""
        pass

    @abstractmethod
    def remember(self, state, action, reward, next_state, done):
        """Commit the given data to memory."""
        pass

    @abstractmethod
    def train_short_memory(self, state, action, reward, next_state, done):
        """Train the model according to its short term memory."""
        pass

    @abstractmethod
    def set_epsilon(self, epsilon):
        """Set the randomness factor for this learning agent."""
        pass


class RandomAgent(Agent):
    """Implements virtually no methods, instead opting to choose moves at random for testing purposes."""

    def set_epsilon(self, epsilon):
        pass

    def make_choice(self, game_state):
        return np.random.randint(4)

    def set_reward(self, reward):
        pass

    def dump_weights(self):
        pass

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_short_memory(self, state, action, reward, next_state, done):
        pass


# TODO(matthew-c21) - Finish implementing this model.
class DefaultAgent:
    def __init__(self):
        self.reward = 0
        self.gamma = 0
        self.data_frame = pd.DataFrame()
        self.short_memory = np.array([])
        self.agent_target = 1
        self.agent_predict = 0
        self.learning_rate = 0.00005
        self.model = self.network()  # Note: this may be set with weights.
        self.epsilon = 0
        self.actual = []
        self.memory = []

    def get_state(self, board, snake):
        state = np.zeros((board.width, board.length))

        for ((x, y), _, value) in board.food_items:
            state[x][y] = value * 10

        for ((x, y), _) in snake:
            state[x][y] = 1

        return state

    def set_reward(self, board, snake):
        if not board.is_playable():
            self.reward -= 100
        elif snake.head.has_eaten:
            self.reward += 10

        return self.reward

    def network(self, weights=None):
        # Shamelessly stolen from https://github.com/maurock/snake-ga/blob/master/DQN.py.
        model = Sequential()
        model.add(Dense(output_dim=120, activation='relu', input_dim=11))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=3, activation='softmax'))
        opt = Adam(self.learning_rate)
        model.compile(loss='mse', optimizer=opt)

        if weights:
            model.load_weights(weights)
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay_new(self, memory):
        if len(memory) > 1000:
            minibatch = random.sample(memory, 1000)
        else:
            minibatch = memory
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
            target_f = self.model.predict(np.array([state]))
            target_f[0][np.argmax(action)] = target
            self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)

    def train_short_memory(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = reward + self.gamma * np.amax(self.model.predict(next_state.reshape((1, 11)))[0])
        target_f = self.model.predict(state.reshape((1, 11)))
        target_f[0][np.argmax(action)] = target
        self.model.fit(state.reshape((1, 11)), target_f, epochs=1, verbose=0)
