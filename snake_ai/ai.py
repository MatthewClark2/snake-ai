from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import random
import numpy as np
import pandas as pd
from operator import add


# TODO(matthew-c21) - Hook up this model so it may be trained.
class Agent:
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
        # TODO(matthew-c21) - Ensure that the GameState class has this method or an equivalent.
        if board.in_terminal_state():
            self.reward -= 10
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

# Main loop
