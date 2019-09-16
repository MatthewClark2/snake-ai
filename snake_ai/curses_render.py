import render
import curses


class TerminalRenderer(render.Renderer):
    # TODO(matthew-c21): Come up with some kind of visual customization options.
    """Renders snake to the terminal using the ncurses library. This class should be utilized inside of the curses.wrapper method to avoid any lingering modifications to terminal function."""

    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)



    def _render(self, snake, food_items):
        self.stdscr.clear()

        for part in snake:
            x, y = part.pos
            self.stdscr.addstr(y, x, "o")

        for food in food_items:
            x, y = food.pos
            self.stdscr.addstr(y, x, "x")


    def render(self, game_state):
        self.stdscr.clear()

        # TODO(matthew-c21): This currently assumes that both the game state is a matrix representing the screen, and that spaces are 0.
        for x, row in game_state:
            for y, val in row:
                if v < 0:  # Snake part
                    self.stdscr.addstr(y, x, "o")
                elif v > 0:  # Food
                    self.stdscr.addstr(y, x, "x")

        self.stdscr.refresh()


    def replay(self, initial_state, moves, food_states, replay_speed):
        # TODO(matthew-c21): This implementation implies the existence of just one food. Fix that so it's less limited.
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
