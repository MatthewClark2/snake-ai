import keras

import ai
import core
from render import TerminalRenderer

import numpy as np
import time


MAX_EPSILON = 200  # Hardcoded value based on example code.


def determine_reward(old_state, new_state):
    # TODO(matthew-c21): Implement.
    return 0


def to_move(move):
    if move[0] == 1:
        return core.UP
    elif move[1] == 1:
        return core.DOWN
    elif move[2] == 1:
        return core.LEFT
    else:
        return core.RIGHT


def main(*args):
    agent = ai.RandomAgent()

    init_dir = core.LEFT
    length = 10
    width = 10
    snake = core.Snake((width // 2, length // 2), 1, init_dir)
    state = core.GameState(snake, length, width)
    renderer = TerminalRenderer()

    # A do-while loop would be nice here.
    renderer.render(state)

    # TODO(matthew-c21): Put inside of another game loop that runs multiple games over the same agent.
    # TODO(matthew-c21): Consider limiting the time the model can go without eating. May need to implement in GameState.
    while state.is_playable():
        # Set epsilon.
        agent.set_epsilon(100)

        old_state = state.to_matrix()

        if np.random.randint(MAX_EPSILON):
            move = keras.utils.to_categorical(np.random.randint(4), num_classes=4)
        else:
            prediction = agent.make_choice(old_state)
            move = keras.utils.to_categorical(prediction, num_classes=4)

        move = to_move(move)

        state.update(move)
        new_state = state.to_matrix()
        reward = determine_reward(old_state, new_state)
        agent.set_reward(reward)

        agent.train_short_memory(old_state, move, reward, new_state, state.is_playable())

        agent.remember(old_state, move, reward, new_state, state.is_playable())

        # TODO(matthew-c21): Enable rendering with a command line flag.
        # TODO(matthew-c21): If rendering, slow it down.
        renderer.render(state)
        time.sleep(0.5)

    renderer.close()


if __name__ == '__main__':
    main()
