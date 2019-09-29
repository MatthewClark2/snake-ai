import render
import curses


class TerminalRenderer(render.Renderer):
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


    def asyncKeys(self, value):
        self.stdscr.nodelay(value)


    def getKey(self):
        """Lock and wait for the next keypress from the terminal. This can be used to have an interactive game
         environment. The sycnhonousness of this function depends on whether or not this object has been called with
         `asyncKeys(True)`."""
        return self.stdscr.getch()
