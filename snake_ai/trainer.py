import argparse
import logging
import sys
import pygame

import numpy as np
import tensorflow.compat.v1 as tf
from keras.utils import to_categorical

import ai
import core
from render import PygameRenderer

MAX_EPSILON = 100  # Hardcoded value based on example code.


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', default=20, type=int, dest='size')
    parser.add_argument('--display', default='1', type=int, dest='display')
    parser.add_argument('--count', default=10, type=int, dest='count')
    parser.add_argument('--init-dir', default='left', dest='init_dir', choices=['up', 'down', 'left', 'right'])
    parser.add_argument('--speed', default=2, type=int, dest='speed')

    return parser.parse_args(args)


def determine_reward(old_state, new_state, playable, min_distance=None):
    """Determines a reward in the range [-1, 1]. Eating returns 1, while dying returns -1. Any other rewards are based
    on the distance to the nearest food item.

    :param old_state the state before the move was taken.
    :param new_state the state of the game after a move was taken.
    :param playable boolean determining whether or not the new state is playable.
    :param min_distance a value in [0, 1) determining how close the nearest food item is."""
    # Punish game over.
    if not playable:
        return -1
    elif new_state[1] == 1:
        return 1

    return -min_distance


def to_move(move, facing):
    """Determines the absolute direction of motion given a relative movement and facing direction.
    :param move an integer corresponding to the relative motion of the snake.
        - 0 is straight.
        - 1 is left.
        - 2 is right
        Other values are considered to be undefined.
    :param facing one of UP, DOWN, LEFT, or RIGHT from the `snake_ai.core` module.
    :returns the absolute direction after applying the given relative motion."""
    if move == 0:
        return facing
    elif move == 1:
        x, y = facing
        return np.array([y, -x])  # Left rotation
    elif move == 2:
        x, y = facing
        return np.array([-y, x])  # Right rotation


def reshape(matrix):
    return matrix  # .reshape((length, -1))


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

    # Shows one game per every games_shown games.
    games_shown = args.display
    moves_per_second = args.speed
    max_drought = length * width

    clock = pygame.time.Clock()

    renderer = None
    if games_shown != 0:
        renderer = PygameRenderer(length, width, 20)

    # TODO(matthew-c21): This value changes in response to state.food_max.
    agent = ai.DefaultAgent((1,), learning_rate=0.0001, gamma=0.01)

    facing = init_dir

    high_score = 0

    for i in range(1, n + 1):  # Number games from 1 to simplify math.
        rendering = games_shown != 0 and i % games_shown == 0

        snake = core.Snake((width // 2, length // 2), length // 4, init_dir)
        state = core.GameState(snake, length, width, max_drought=max_drought, food_max=1)

        logging.info('Starting game ' + str(i))

        while state.is_playable():
            # Decrease epsilon over time.
            agent.set_epsilon(max(MAX_EPSILON - i, 0))

            old_state = reshape(state.get_primitive_state_vector())

            if np.random.randint(MAX_EPSILON) < agent.epsilon:
                move = np.random.randint(3)
                logging.info('Generated: ' + str(move))
            else:
                # skip prediction for previous state. Output is dim[0], 3
                prediction = agent.make_choice(np.array(old_state))[0]

                move = np.argmax(prediction)

                logging.info('Predicted: ' + str(move))

            move = to_move(move, facing)
            facing = move
            state.update(move)

            new_state = reshape(state.get_primitive_state_vector())
            scaled_distance = 0.0001  # np.linalg.norm(snake.head().pos - state.food_items[0].pos) / max_distance
            reward = determine_reward(old_state, new_state, state.is_playable(), scaled_distance)

            logging.info('Reward for move: ' + str(reward))

            agent.remember(old_state, move, reward, new_state, 1 if state.is_playable() else 0)
            agent.train_short_memory(old_state, move, reward, new_state, 1 if state.is_playable() else 0)

            if rendering:
                frame_count = 0
                while frame_count < (60 / moves_per_second):
                    frame_count += 1
                    renderer.render(state)
                    clock.tick(60)

        agent.replay_new()
        high_score = max(high_score, state.get_score())

    if games_shown != 0:
        renderer.close()

    print('Max score achieved: ', high_score)


if __name__ == '__main__':
    # Overwrite the logfile every time that training begins.
    logging.basicConfig(filename='training.log', filemode='w', level=logging.INFO)
    logging.info('Starting training.')

    main(sys.argv[1:])
