import curses
import time
import pygame
import numpy as np
from abc import ABC, abstractmethod


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
    def replay(self, initial_state, moves, replay_speed):
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

    @abstractmethod
    def clear(self):
        """Clear the screen."""
        pass


class TerminalRenderer(Renderer):
    # TODO(matthew-c21): Come up with some kind of visual customization options.
    """Renders snake to the terminal using the ncurses library. This class should be utilized inside of the
    curses.wrapper method to avoid any lingering modifications to terminal function."""

    def clear(self):
        self.stdscr.clear()

    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

    def render(self, game_state, game_count=None):
        self.stdscr.clear()

        # TODO(matthew-c21): This currently assumes that both the game state is a matrix representing the screen, and
        #  that spaces are 0.
        max_x, max_y = game_state.size()
        matrix = game_state.to_matrix()

        # Render corners.
        self.stdscr.addstr(0, 0, '+')
        self.stdscr.addstr(max_y, 0, '+')
        self.stdscr.addstr(max_y, max_x, '+')
        self.stdscr.addstr(0, max_x, '+')

        # Render vertical walls.
        for i in range(1, max_y):
            self.stdscr.addstr(i, 0, '|')
            self.stdscr.addstr(i, max_x, '|')

        # Render horizontal walls.
        for i in range(1, max_x):
            self.stdscr.addstr(0, i, '-')
            self.stdscr.addstr(max_y, i, '-')

        # Render snake and food.
        for y in range(max_x):
            row = matrix[y]
            for x, val in enumerate(row):
                if val < 0:  # Snake part
                    self.stdscr.addstr(y, x, "o")
                elif val > 0:  # Food
                    self.stdscr.addstr(y, x, "x")

        # Render debugging info.
        self.stdscr.addstr(0, max_x + 4, "Head pos: " + str(game_state.snake.head().pos))
        self.stdscr.addstr(max_y // 3, max_x + 4, "Playable? " + str(game_state.is_playable()))
        self.stdscr.addstr(max_y - 1, max_x + 4, "Score: " + str(game_state.get_score()))

        if game_count is not None:
            self.stdscr.addstr(2 * max_y // 3, max_x + 4, "Game " + str(game_count))

        # Actually draw to screen.
        self.stdscr.refresh()

    def replay(self, initial_state, moves, replay_speed):
        delay = 1 / replay_speed

        # Render the initial state.
        self.render(initial_state)

        for move in moves:
            initial_state.update(move)
            self.render(initial_state)
            time.sleep(delay)

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


class PygameRenderer(Renderer):
    """Pygame renderer focused around only having a single food type on screen.
    This class does not manage its own clock."""
    def __init__(self, length, width, block_size):
        pygame.font.init()
        self.block_size = block_size
        self.length = length
        self.width = width
        self.text_area_start = (width + 1) * block_size + 50
        self.font = pygame.font.SysFont('Arial', 24)
        self.window = pygame.display.set_mode((self.text_area_start + 150, (length + 1) * block_size))

    def render(self, game_state):
        self.window.fill((255, 255, 255))

        for segment in game_state.snake:
            (x, y) = self.block_size * np.array(segment.pos)
            r = pygame.Rect((x, y), (self.block_size, self.block_size))
            pygame.draw.rect(self.window, (0, 255, 0), r)

        for segment in game_state.food():
            (x, y) = self.block_size * np.array(segment.pos)
            r = pygame.Rect((x, y), (self.block_size, self.block_size))
            pygame.draw.rect(self.window, (255, 0, 0), r)

        text_surface = self.font.render('Score: ' + str(game_state.get_score()), False, (0, 0, 0))
        self.window.blit(text_surface, (self.text_area_start, self.length * self.block_size // 2))

        # Add a rectangle around the play area.
        r = pygame.Rect(0, 0, (self.width + 1) * self.block_size, (self.length + 1) * self.block_size)

        pygame.draw.rect(self.window, (0, 0, 0), r, 1)

        pygame.display.update()

    def replay(self, initial_state, moves, replay_speed):
        # Render the initial state.
        self.render(initial_state)

        for move in moves:
            initial_state.update(move)
            self.render(initial_state)

    def close(self):
        pygame.quit()

    def clear(self):
        self.window.fill((255, 255, 255))
