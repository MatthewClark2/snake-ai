import core
import curses
from curses_render import TerminalRenderer


def main(*args):
    length = 10
    width = 10
    snake = core.Snake((width//2, length//2), width // 4, core.LEFT)
    state = core.GameState(snake, length, width)
    print(state.to_matrix())
    print(snake)
    # renderer = TerminalRenderer()

    # Put into a while loop.
    # Get inputs from renderer.
    # Feed inputs to state.
    # renderer.render(state)
    # renderer.getKey()  # Wait for a keypress to end the game.
    # renderer.close()


if __name__ == '__main__':
    main()
    # curses.wrapper(main)
