import keras
import tensorflow.compat.v1 as tf

import ai
import core
from render import TerminalRenderer

import numpy as np
import time


MAX_EPSILON = 200  # Hardcoded value based on example code.


def determine_reward(old_state, new_state, playable, movement_reward=0):
    # Punish game over.
    if not playable:
        return -100

    # Reward eating.
    for y, row in enumerate(old_state - new_state):
        for x, val in enumerate(row):
            if val > 0 and old_state[y, x] > 0:  # Head of snake occupies position where food used to be.
                return old_state[y, x]

    # Reward or punish survival.
    return movement_reward


def to_move(move):
    if move[0] == 1:
        return core.UP
    elif move[1] == 1:
        return core.DOWN
    elif move[2] == 1:
        return core.LEFT
    else:
        return core.RIGHT


def reshape(matrix):
    return matrix.reshape((1, -1))


def main(*args):
    # Suppress all non-vital tensorflow warnings.
    tf.logging.set_verbosity(tf.logging.ERROR)

    n = 10
    length = 20
    width = 20
    dim = (length + 1) * (width + 1)
    init_dir = core.LEFT
    rendering = True

    renderer = None
    if rendering:
        renderer = TerminalRenderer()

    agent = ai.DefaultAgent(dim)

    for i in range(n):
        snake = core.Snake((width // 2, length // 2), length // 4, init_dir)
        state = core.GameState(snake, length, width)

        while state.is_playable():
            if rendering:
                # TODO(matthew-c21): Enable rendering with a command line flag.
                renderer.render(state, i)
                # TODO(matthew-c21): Update sleep delay in order to reduce stuttering.
                time.sleep(0.25)

            # TODO(matthew-c21): Consider limiting the time the model can go without eating.
            #  May need to implement in GameState.
            # Decrease epsilon over time.
            agent.set_epsilon(100 - i)

            old_state = state.to_matrix()
            old_col = reshape(old_state)

            if np.random.randint(MAX_EPSILON) < agent.epsilon:
                move = keras.utils.to_categorical(np.random.randint(4), num_classes=4)
            else:
                prediction = agent.make_choice(old_col)
                move = keras.utils.to_categorical(prediction, num_classes=4)[0][0]

            move = to_move(move)
            state.update(move)

            new_state = state.to_matrix()
            new_col = reshape(new_state)
            reward = determine_reward(old_state, new_state, state.is_playable())

            agent.set_reward(reward)

            # TODO(matthew-c21): Consider training between games rather than on every move. This allows for a full test
            #  of a given set of weights rather than shuffling them every time.
            agent.train_short_memory(old_col, move, reward, new_col, state.is_playable())

            agent.remember(old_col, move, reward, new_col, state.is_playable())

        agent.replay_new()

    renderer.close()


if __name__ == '__main__':
    main()
