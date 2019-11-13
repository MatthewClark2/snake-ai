import argparse
import logging
import sys
import pygame

import numpy as np
import tensorflow.compat.v1 as tf

import ai
import core
from render import PygameRenderer


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', default=20, type=int, dest='size')
    parser.add_argument('--display', default='1', type=int, dest='display')
    parser.add_argument('--count', default=10, type=int, dest='count')
    parser.add_argument('--init-dir', default='left', dest='init_dir', choices=['up', 'down', 'left', 'right'])
    parser.add_argument('--speed', default=2, type=int, dest='speed')

    return parser.parse_args(args)


def determine_reward(playable, min_distance, has_eaten):
    """Determines a reward in the range [-1, 1]. Eating returns 1, while dying returns -1. Any other rewards are based
    on the distance to the nearest food item.

    :param playable boolean determining whether or not the new state is playable.
    :param min_distance a value in [0, 1) determining how close the nearest food item is.
    :param has_eaten a boolean determining whether or not the previous move resulted in eating."""
    # Punish game over.
    if not playable:
        return -1
    elif has_eaten:
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
    # The input must be re-wrapped into a numpy array to be recognized correctly.
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

    # Shows one game per every games_shown games.
    games_shown = args.display
    moves_per_second = args.speed
    max_drought = length * width

    clock = pygame.time.Clock()

    renderer = None
    if games_shown != 0:
        renderer = PygameRenderer(length, width, 20)

    # TODO(matthew-c21): This value changes in response to state.food_max.
    agent = ai.DefaultAgent((9,), epsilon=0.5, gamma=0.95)

    facing = init_dir

    high_score = 0

    # TODO(matthew-c21): Try to add replay for best game in set to see whether or not the AI has actually improved, or
    #  if the result was a fluke. Consider storing more than one game if only the first (and / or second) best instances
    #  were accidental.

    # TODO(matthew-c21): Add option to save weights at end of training, or to load weights at start.
    for i in range(1, n + 1):  # Number games from 1 to simplify math.
        rendering = games_shown != 0 and i % games_shown == 0

        snake = core.Snake((width // 2, length // 2), 4, init_dir)
        state = core.GameState(snake, length, width, max_drought=max_drought, food_max=1)

        print('Game: %d, ' % i, end='')
        logging.info('Starting game ' + str(i))

        while state.is_playable():
            old_state = reshape(state.get_primitive_state_vector())

            action = agent.make_choice(old_state)

            move = to_move(action, facing)
            facing = move
            has_eaten = state.update(move)

            new_state = reshape(state.get_primitive_state_vector())
            scaled_distance = 0  # distance(snake.head().pos, state.food_items[0].pos) / max_drought
            reward = determine_reward(state.is_playable(), scaled_distance, has_eaten)

            logging.info('Reward for move %d: %f' % (action, reward))

            agent.train_short_memory(old_state, action, reward, new_state, state.is_playable())
            agent.remember(old_state, action, reward, new_state, state.is_playable())

            if rendering:
                frame_count = 0
                while frame_count < (60 / moves_per_second):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            renderer.close()
                            handle_game_over(high_score)
                            sys.exit(0)
                    frame_count += 1
                    renderer.render(state)
                    clock.tick(60)
            elif renderer is not None:
                renderer.clear()

        print('Score: %d' % state.get_score())
        agent.replay_new()
        high_score = max(high_score, state.get_score())

    handle_game_over(high_score)


def handle_game_over(high_score):
    print('Max score achieved: ', high_score)


def distance(p1, p2):
    p = p1 - p2
    return np.sqrt(p[0] ** 2 + p[1] ** 2)


if __name__ == '__main__':
    # Overwrite the logfile every time that training begins.
    logging.basicConfig(filename='training.log', filemode='w', level=logging.WARN)
    logging.info('Starting training.')

    main(sys.argv[1:])
