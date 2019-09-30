import curses
from abc import ABC, abstractmethod

# TODO(matthew-c21): Move all renderers into this file.
# TODO(matthew-c21): Have all renderers show debugging information about the game state rather than just a raw cut of it


class Renderer(ABC):
    """Showing the game itself requires some level of persistent resources as well as actual rendering logic. This class
    serves as the basis for all implementations."""
    @abstractmethod
    def render(self, game_state):
        """Render the current game state as is. This method should recycle any resources currently in use by the
        renderer.

        Arguments
        game_state: the current state to be rendered."""
        pass

    @abstractmethod
    def replay(self, initial_state, moves, food, replay_speed):
        """Given an initial game state and a list of moves, play back the game from start to the point at which moves
        are no longer given.

        Arguments
        initial_state: An instance of GameState representing the initial state of the game.
        moves: the list of movements (UP, DOWN, LEFT, RIGHT) representing the movements taken during the game.
        food: list of tuples in the form (turn, food) representing when food appears as well as the food itself.
        replay_speed: the number of moves to be taken per second."""
        pass

    @abstractmethod
    def close(self):
        """Discard any allocated resources associated with the rendering process."""
        pass


class TerminalRenderer(Renderer):
    # TODO(matthew-c21): Come up with some kind of visual customization options.
    """Renders snake to the terminal using the ncurses library. This class should be utilized inside of the
    curses.wrapper method to avoid any lingering modifications to terminal function."""

    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

    def render(self, game_state):
        self.stdscr.clear()

        # TODO(matthew-c21): This currently assumes that both the game state is a matrix representing the screen, and
        #  that spaces are 0.
        for x, row in enumerate(game_state.to_matrix()):
            for y, val in enumerate(row):
                if val < 0:  # Snake part
                    self.stdscr.addstr("o")
                elif val > 0:  # Food
                    self.stdscr.addstr("x")
                else:
                    self.stdscr.addstr(" ")
            self.stdscr.addstr("\n")

        self.stdscr.refresh()

    def replay(self, initial_state, moves, food_states, replay_speed):
        # TODO(matthew-c21): This implementation implies the existence of just one food. Fix that so it's less limited.
        # TODO(matthew-c21): Conceptually fixed via the introduction of seeded RNG.
        state = initial_state
        curr_food = 0
        t, food = food_states[curr_food]

        for i, move in moves:
            if i == t:
                state.set_food([food])
                curr_food += 1
                t, food = food_states[curr_food]

            state.update(move)

    def close(self):
        curses.echo()
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.endwin()

    def async_keys(self, value):
        self.stdscr.nodelay(value)

    def get_key(self):
        """Lock and wait for the next keypress from the terminal. This can be used to have an interactive game
         environment. The synchronicity of this function depends on whether or not this object has been called with
         `asyncKeys(True)`."""
        return self.stdscr.getch()