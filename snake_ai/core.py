"""Contains main game logic."""
from collections import deque, namedtuple

import numpy as np

UP = np.array([0, -1])
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
        self.facing = self.fix_dir(direction)

        self.body.appendleft(_snake_part(self.head().pos + self.facing, has_eaten))

        if not self.body[-1].has_eaten:
            self.body.pop()
        else:
            self.body[-1] = _snake_part(self.body[-1].pos, False)

    def intersects(self, position, start_pos=0):
        """Helper method to determine if a position makes contact with this snake."""
        for part in list(self)[start_pos:]:
            if (part.pos == position).all():
                return True

        return False

    def head(self):
        return self.body[0]

    def __len__(self):
        return len(self.body)

    def fix_dir(self, direction):
        if (direction + self.facing == np.zeros(2)).all():
            return self.facing
        return direction


# TODO(matthew-c21) - Extract an abstract class to simplify later board designs.
class GameState:
    """Primitive board implementation.

    No internal walls, outer perimeter acts as border, only one food item on screen at a time."""

    def __init__(self, snake, length, width, food_max=1, seed=None, max_drought=np.Inf):
        self.length = length
        self.width = width
        self.snake = snake
        self.food_max = food_max
        self.food_items = []
        self.score = 0
        self.max_drought = max_drought
        self.turn_count = 0
        self.state_flag = True
        self.prev_move = None
        self.seed = seed if seed is not None else np.random.randint(2 ** 32)  # Hardcoded value for maximum seed.
        self._update_food()

    # TODO(matthew-c21): Have the board generate it's own snake given a relative size and initial facing direction.
    def update(self, direction):
        """Updates the game state in accordance with the given move. If the game is not in a playable state, no changes
        will occur."""

        if not self.state_flag:
            return False

        # TODO(matthew-c21): Reset turn count after eating. Add corresponding tests.
        self.turn_count += 1

        has_eaten = False

        updated_pos = self.snake.fix_dir(direction) + self.snake.head().pos
        self.prev_move = self.snake.fix_dir(direction)

        for food in self.food_items:
            if (food.pos == updated_pos).all():
                has_eaten = True
                self.turn_count = 0
                break
        # has_eaten = any(self.snake.intersects(food.pos) for food in self.food_items)
        self.snake.move(direction, has_eaten)

        updated_position = self.snake.head().pos

        self.seed += direction[0] * 10 + direction[1]
        self.seed %= 2 ** 32

        # TODO(matthew-c21): Ensure that all food items have unique positions so this loop doesn't execute more than
        #  once. Consider a map using position tuples as keys.
        for i, food in enumerate(self.food_items[::-1]):
            if self.snake.intersects(food.pos):
                self.score += food.value
                self.food_items = self.food_items[:self.food_max-i-1] + self.food_items[self.food_max-i:]

        self._update_food()

        if self.snake.intersects(updated_position, 1) or \
                self._out_of_bounds(updated_position) or \
                self.turn_count > self.max_drought:
            self.state_flag = False

        # TODO(matthew-c21): Test return value.
        return has_eaten

    def _update_food(self):
        np.random.seed(self.seed)
        while len(self.food_items) < self.food_max:
            # TODO(matthew-c21) - Optimize the selection algorithm to avoid possible slowdowns.
            # 100 is just a hard-coded value for all food items.
            new_food = _food_item(np.array([np.random.randint(1, n) for n in (self.width, self.length)]), 1)
            if self.snake.intersects(new_food.pos):
                continue

            self.food_items.append(new_food)

    def _out_of_bounds(self, position):
        x, y = position
        if x <= 0 or x >= self.width or y <= 0 or y >= self.length:
            return True
        return False

    def set_food(self, food):
        self.food_items = food
        self._update_food()

    def get_score(self):
        return self.score

    def is_playable(self):
        return self.state_flag

    def size(self):
        return self.width, self.length

    def food(self):
        return self.food_items

    def to_matrix(self):
        # TODO(matthew-c21): Update tests and rendering to recognize walls being negative rather than 0.
        # TODO(matthew-c21): This represents game state, so it can probably be simplified to food and snake locations
        #  rather than including empty space.
        matrix = np.zeros((self.length + 1, self.width + 1))  # Add 1 since OOB is at width/length.

        # Make walls negative as well.
        for i in range(self.width):
            matrix[i, 0] = -1
            matrix[i, self.length] = -1

        for i in range(self.length):
            matrix[0, i] = -1
            matrix[self.width, i] = -1

        for part in self.snake:
            x, y = part.pos
            matrix[y, x] = -100  # numpy matrices are accessed row, column

        for food in self.food_items:
            x, y = food.pos
            matrix[y, x] = food.value

        return matrix

    def get_primitive_state_vector(self):
        # TODO(matthew-c21): Unit test this method.
        facing = self.snake.facing
        pos = self.snake.head().pos
        x, y = facing
        ahead = facing + pos
        left = np.array([y, -x]) + pos
        right = np.array([-y, x]) + pos

        vector = [
            self.snake.intersects(ahead) or self._out_of_bounds(ahead),
            self.snake.intersects(left) or self._out_of_bounds(left),
            self.snake.intersects(right) or self._out_of_bounds(right),
            (self.prev_move == UP).all(),
            (self.prev_move == LEFT).all(),
            (self.prev_move == RIGHT).all(),
        ]

        vector = np.hstack([  # pos - self.food_items[0].pos,
                            pos < self.food_items[0].pos,
                            vector])

        return np.array([1 if x else 0 for x in vector])

    def min_distance_to_food(self):
        # TODO(matthew-c21): Return both the scalar and vector. Prepend the vector to the linearized matrix
        #  representation.
        distances = []
        for food in self.food_items:
            distances.append(np.linalg.norm(self.snake.head().pos - food.pos))

        return min(distances)

    def get_seed(self):
        return self.seed
