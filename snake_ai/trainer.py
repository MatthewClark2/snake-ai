import argparse
import sys
import time

import keras
import numpy as np
import tensorflow.compat.v1 as tf

import ai
import core
from render import TerminalRenderer

MAX_EPSILON = 200  # Hardcoded value based on example code.


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', default=20, type=int, dest='size')
    parser.add_argument('--display', default='1', type=int, dest='display')
    parser.add_argument('--count', default=10, type=int, dest='count')
    parser.add_argument('--init-dir', default='left', dest='init_dir', choices=['up', 'down', 'left', 'right'])
    parser.add_argument('--speed', default=2, type=int, dest='speed')
    parser.add_argument('--punish-movement', action='store_true', default=False, dest='punish_movement')

    return parser.parse_args(args)


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


def main(args=None):
    # Suppress all non-vital tensorflow warnings.
    tf.logging.set_verbosity(tf.logging.ERROR)

    args = parse_args(args)

    n = args.count
    length = args.size
    width = length  # Default to being square. This may be changed in the future.
    init_dir = {
        'up': core.UP,
        'down': core.DOWN,
        'left': core.LEFT,
        'right': core.RIGHT,
    }[args.init_dir]

    move_value = 1 if args.punish_movement else 0

    # Shows one game per every games_shown games.
    games_shown = args.display

    moves_per_second = args.speed
    base_delay = 1 / moves_per_second

    dim = (length + 1) * (width + 1)
    max_drought = length * width

    renderer = None
    if games_shown != 0:
        renderer = TerminalRenderer()

    agent = ai.DefaultAgent(dim)

    for i in range(1, n + 1):  # Number games from 1 to simplify math.
        rendering = games_shown != 0 and i % games_shown == 0

        snake = core.Snake((width // 2, length // 2), length // 4, init_dir)
        state = core.GameState(snake, length, width, max_drought=max_drought)

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
            reward = -determine_reward(old_state, new_state, state.is_playable(), move_value)

            agent.train_short_memory(old_col, move, reward, new_col, state.is_playable())
            agent.remember(old_col, move, reward, new_col, state.is_playable())

            if rendering:
                renderer.render(state, i)
                elapsed_time = time.time() - loop_start
                time.sleep(base_delay - elapsed_time % base_delay)

        agent.replay_new()

    if games_shown != 0:
        renderer.close()

    print(agent.dump_weights())


if __name__ == '__main__':
    main(sys.argv[1:])
