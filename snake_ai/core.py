"""Contains main game logic."""

import numpy as np
from collections import deque, namedtuple


UP = np.array([0, 1])
DOWN = -UP
LEFT = np.array([-1, 0])
RIGHT = -LEFT


# Helper class to clarify each segment of a snake.
_snake_part = namedtuple('snake_part', ['pos', 'has_eaten'])
_food_item = namedtuple('food_item', ['pos', 'value'])


class Snake:
    def __init__(self, start_pos, init_length, facing):
        """Generate a new snake according to the given specifications. The tail of the snake will be
        generated in a straight line behind the head.

        Arguments:
        start_pos: initial position of the head given as a numpy array.
        init_length: scalar quantity representing the length of the snake including the head.
        facing: UP, DOWN, LEFT, or RIGHT in this package."""

        self.body = deque()  # The tail is stored at the head of the queue.
        self.facing = facing
        for i in range(init_length):
            self.body.append(_snake_part(start_pos - i * facing, False))

        self.length = init_length


    def __iter__(self):
        """Return an iterator that begins at the head of the snake and moves to the tail.

        Each value yielded is a named tuple in the form (position, direction), with both values
        being two-value vectors represented by np.ndarray."""
        return iter(self.body)


    def __str__(self):
        return '\n'.join([str(part) for part in self])


    def move(self, direction, has_eaten=False):
        """Cause the snake to change it's direction, adjusting the rest of the body forward.

        If the provided direction is the opposite of the facing direction, then the snake will just
        more forward. For example, if a snake is facing right and made to move left, then it will
        continue to move right.

        Arguments:
        direction: one of UP, DOWN, LEFT, or RIGHT. The new direction for the head of the snake to
            face.
        should_extend: boolean determining whether or not the snake should grow due to the tile it
        has traversed."""
        if (self.facing + direction == np.zeros(2)).all():
            direction = self.facing

        self.body.appendleft(_snake_part(self.head().pos + direction, has_eaten))

        if not self.body[-1].has_eaten:
            self.body.pop()


    # TODO(matthew-c21): Test intersections.
    def intersects(self, position, start_pos=0):
        print(position)
        print(start_pos)
        """Helper method to determine if a position makes contact with this snake."""
        for i in range(1, len(self.body)):
            if (position == self.body[i].pos).all():
                return True

        return False
        # return any(position == p.position for p in self.body[start_pos:])


    def head(self):
        return self.body[0]


    def __len__(self):
        return len(self.body)


#TODO(matthew-c21) - Extract an abstract class to simplify later board designs.
# TODO(matthew-c21): Give it a seedable RNG for well-behaved replays.
class GameState:
    """Primitive board implementation.

    No internal walls, outer perimeter acts as border, only one food item on screen at a time."""
    def __init__(self, snake, length, width):
        self.length = length
        self.width = width
        self.snake = snake
        self.food_max = 1
        self.food_items = []
        self.previous_position = snake.head().pos
        self.score = 0
        self._update_food()


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
        while len(self.food_items) < self.food_max:
            # TODO(matthew-c21) - Optimize the selection algorithm to avoid possible slowdowns.
            new_food = _food_item([np.random.randint(n) for n in (self.width, self.length)], 100)  # 100 is just a hard-coded value for all food items.
            if self.snake.intersects(new_food.pos):
                continue

            self.food_items.append(new_food)


    def _out_of_bounds(self, position):
        return 0 <= position[0] < self.width and 0 <= position[1] < self.length


    def set_food(self, new_food):
        """Manually set the location of all food on screen, either for debugging or replay purposes."""
        # TODO(matthew-c21): Validate the new food inputs.
        self.food_items = new_food


    def score(self):
        return self.score


    def size(self):
        return width, length


    def to_matrix(self):
        # TODO(matthew-c21): Test the output of this method.
        # TODO(matthew-c21): This represents game state, so it can probably be simplified to food and snake locations rather than including empty space.
        # TODO(matthew-c21): Since this matrix represents both game state and possible reward of interaction, consider penalizing non-food movement.
        matrix = np.zeros((self.length, self.width))
        for part in self.snake:
            x, y = part.pos
            matrix[y, x] = -100  # numpy matrices are accessed row, column
            # matrix[np.array(part.pos, dtype=np.int32)] = -100

        for food in self.food_items:
            x, y = food.pos
            matrix[y, x] = food.value
            # matrix[food.pos[0]][food.pos[1]] = food.value

        return matrix
