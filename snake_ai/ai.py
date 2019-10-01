import random
from abc import ABC, abstractmethod

import numpy as np
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

    def dump_weights(self):
        pass

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_short_memory(self, state, action, reward, next_state, done):
        pass


# TODO(matthew-c21) - Finish implementing this model.
class DefaultAgent(Agent):
    def __init__(self, input_dim, learning_rate=0.00005, epsilon=0, gamma=0, weights=None):
        self.input_dim = input_dim
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.gamma = gamma
        self.memory = []
        self.short_memory = np.array([])
        self.model = DefaultAgent._network(learning_rate, input_dim, weights=weights)

    def make_choice(self, game_state):
        # TODO(matthew-c21): Determine if more configuration needed.
        return self.model.predict(game_state)

    def dump_weights(self):
        return self.model.get_weights()

    def set_epsilon(self, epsilon):
        self.epsilon = epsilon

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_short_memory(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = reward + self.gamma * np.amax(self.make_choice(next_state)[0])

        target_f = self.make_choice(state)
        target_f[0][np.argmax(action)] = target
        self.model.fit(state, target_f, epochs=1, verbose=0)

    def replay_new(self, max_sample=1000):
        """Retrain the model based on a sampling of its own memory."""
        # TODO(matthew-c21): Determine how this actually works.
        if len(self.memory) > max_sample:
            batch = random.sample(self.memory, max_sample)
        else:
            batch = self.memory
        for state, action, reward, next_state, done in batch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.make_choice(state)
            target_f[0][np.argmax(action)] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)

    @staticmethod
    def _network(learning_rate, input_dim, output_dim=120, weights=None):
        # Shamelessly stolen from https://github.com/maurock/snake-ga/blob/master/DQN.py.
        # TODO(matthew-c21): Determine how output_dim affects model.
        model = Sequential()
        model.add(Dense(units=512, activation='relu', input_dim=input_dim))
        model.add(Dropout(0.5))
        model.add(Dense(units=256, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(units=4, activation='softmax'))
        opt = Adam(learning_rate)
        model.compile(loss='mse', optimizer=opt)

        if weights:
            model.load_weights(weights)
        return model
