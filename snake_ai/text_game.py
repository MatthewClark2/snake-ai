import curses

import core
from render import TerminalRenderer


def convert(keycode, default=None):
    return {
        curses.KEY_UP: core.UP,
        curses.KEY_DOWN: core.DOWN,
        curses.KEY_LEFT: core.LEFT,
        curses.KEY_RIGHT: core.RIGHT,
    }.get(keycode, default)


def handle_game_over(game_state):
    with open('log_data.txt') as logfile:
        print(game_state.score, file=logfile)


# TODO(matthew-c21): Add some type of logging because this sure ain't working.
def main(*args):
    init_dir = core.LEFT
    length = 10
    width = 10
    snake = core.Snake((width // 2, length // 2), 1, init_dir)
    state = core.GameState(snake, length, width)
    renderer = TerminalRenderer()

    # Put into a while loop.
    # Get inputs from renderer.
    # Feed inputs to state.

    # A do-while loop would be nice here.
    renderer.render(state)
    input_dir = convert(renderer.get_key(), init_dir)

    while state.is_playable():
        state.update(input_dir)
        renderer.render(state)
        input_dir = convert(renderer.get_key(), input_dir)

    renderer.render(state)
    renderer.get_key()  # Wait for a keypress to end the game.
    renderer.close()


if __name__ == '__main__':
    curses.wrapper(main)
