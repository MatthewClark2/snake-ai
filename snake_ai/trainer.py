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

    # TODO(matthew-c21): Provide a way to only show some games, or just replay decent ones from a training session.
    rendering = True
    moves_per_second = 2  # This seems to be the fastest that the training can be done without notable slowdowns.
    base_delay = 1 / moves_per_second

    renderer = None
    if rendering:
        renderer = TerminalRenderer()

    agent = ai.DefaultAgent(dim)

    for i in range(n):
        snake = core.Snake((width // 2, length // 2), length // 4, init_dir)
        state = core.GameState(snake, length, width)

        while state.is_playable():
            loop_start = time.time()

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
            agent.train_short_memory(old_col, move, reward, new_col, state.is_playable())
            agent.remember(old_col, move, reward, new_col, state.is_playable())

            # TODO(matthew-c21): Enable rendering with a command line flag.
            if rendering:
                renderer.render(state, i)
                elapsed_time = time.time() - loop_start
                time.sleep(base_delay - elapsed_time % base_delay)

        agent.replay_new()

    renderer.close()


if __name__ == '__main__':
    main()
