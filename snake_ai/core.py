"""Contains main game logic."""

import pygame
import numpy as np
from collections import deque, namedtuple


UP = np.array([0, 1])
DOWN = -UP
LEFT = np.array([-1, 0])
RIGHT = -LEFT


# Helper class to clarify each segment of a snake.
_snake_part = namedtuple('snake_part', ['position', 'direction'])
_food_item = namedtuple('food_item', ['position', 'freshness', 'value'])


class Snake:
    def __init__(self, start_pos, init_length, facing):
        """Generate a new snake according to the given specifications. The tail of the snake will be
        generated in a straight line behind the head.

        Arguments:
        start_pos: initial position of the head given as a numpy array.
        init_length: scalar quantity representing the length of the snake including the head.
        facing: UP, DOWN, LEFT, or RIGHT in this package."""

        self.body = deque()  # The tail is stored at the head of the queue.
        for i in range(init_length):
            self.body.append(_snake_part(start_pos - i * facing, facing))

        self.length = init_length


    def __iter__(self):
        """Return an iterator that begins at the head of the snake and moves to the tail.

        Each value yielded is a named tuple in the form (position, direction), with both values
        being two-dimensional vectors represented by np.ndarray."""
        return iter(self.body)


    def __str__(self):
        return '\n'.join([str(part) for part in self])


    def move(self, direction, should_extend=False):
        """Cause the snake to change it's direction, adjusting the rest of the body forward.

        If the provided direction is the opposite of the facing direction, then the snake will just
        more forward. For example, if a snake is facing right and made to move left, then it will
        continue to move right.

        Arguments:
        direction: one of UP, DOWN, LEFT, or RIGHT. The new direction for the head of the snake to
            face.
        should_extend: boolean determining whether or not the snake should grow due to the tile it
        has traversed."""
        if (self.head.direction + direction == np.zeros(2)).all():
            direction = self.head.direction

        self.body.appendleft(_snake_part(self.head.position + direction, direction))

        if not should_extend:
            self.body.pop()


    def intersects(self, position, start_pos=0):
        """Helper method to determine if a position makes contact with this snake."""
        return any(position == p.position for p in body[start_pos:])


    @property
    def head(self):
        return self.body[0]


#TODO(matthew-c21) - Extract an abstract class to simplify later board designs.
class GameState:
    """Primitive board implementation.

    No internal walls, outer perimeter acts as border, only one food item on screen at a time."""
    def __init__(self, snake, length, width):
        self.length = length
        self.width = width
        self.snake = snake
        self.food_max = 1
        self.food_items = []
        self.previous_position = snake.head.position
        self.score = 0


    def update(self, direction):
        """Updates the game state in accordance with the given move, and returns a boolean
        determining whether or not the game is still in a playable state."""
        self._update_food()

        updated_position = self.previous_position + direction

        for food in self.food_items:
            if (food.position == updated_position).all():
                self.score += food.value
                self.snake.move(direction, True)
        else:
                self.snake.move(direction, False)

        return self.snake.intersects(updated_position, 1) or self._out_of_bounds(updated_position)

    def _update_food(self):
        self.food_items = filter(lambda f: f.freshness <= 0, [food_item(f.position, f.freshness - 1)
                                                              for food in self.food_items])

        while len(self.food_items) < self.food_max:
            # TODO(matthew-c21) - Optimize the selection algorithm to avoid possible slowdowns.
            new_food = _food_item([np.random.randint(n) for n in (length, width)], 30, 1)
            if self.snake.intersects(new_food.position):
                continue

            food_items.append(new_food)


    def _out_of_bounds(self, position):
        return position[0] < 0 or position[1] < 0 or position[0] >= length or position[1] >= width


def trigger_game_over(game_state):
    """This is where all game cleanup etc. takes place."""
    pass
