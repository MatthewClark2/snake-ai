import unittest
from itertools import cycle

import numpy as np
import snake_ai.core as core


def assert_snake_has_position(snake, position):
    for i, part in enumerate(snake):
        np.testing.assert_array_equal(part.pos, position[i])


class CoreTest(unittest.TestCase):
    # TODO(matthew-c21): The matrix representation of the game state may be simplified in the future meaning that this
    #  test will have to be changed.
    def _check_matrix(self, snake, state_matrix, food=[]):
        # This is a lot of logic required for testing, but it beats having to hardcode an explicit matrix when there's
        # no specification for the state given that's any clearer than what's given here.
        for i in range(10):
            for j in range(10):
                if snake.intersects(np.array([i, j])):  # Note that positions are x,y, but matrix access is y,x.
                    self.assertTrue(state_matrix[j, i] < -1)
                elif any((f.pos == [i, j]).all() for f in food):
                    self.assertGreater(state_matrix[j, i], 0)
                else:
                    self.assertTrue(-1 <= state_matrix[j, i] <= 0)

    def test_snake_creation_up(self):
        pos = [np.array(x) for x in [(5, 5), (5, 6), (5, 7)]]
        snake = core.Snake(pos[0], 3, core.UP)
        assert_snake_has_position(snake, pos)

    def test_snake_creation_down(self):
        pos = [np.array(x) for x in [(5, 5), (5, 4), (5, 3)]]
        snake = core.Snake(pos[0], 3, core.DOWN)
        assert_snake_has_position(snake, pos)

    def test_snake_creation_left(self):
        pos = [np.array(x) for x in [(5, 5), (6, 5), (7, 5)]]
        snake = core.Snake(pos[0], 3, core.LEFT)
        assert_snake_has_position(snake, pos)

    def test_snake_creation_right(self):
        pos = [np.array(x) for x in [(5, 5), (4, 5), (3, 5)]]
        snake = core.Snake(pos[0], 3, core.RIGHT)
        assert_snake_has_position(snake, pos)

    def test_snake_move_up(self):
        snake_up = core.Snake(np.array([6, 6]), 4, core.UP)
        snake_down = core.Snake(np.array([6, 6]), 4, core.DOWN)
        snake_left = core.Snake(np.array([6, 6]), 4, core.LEFT)
        snake_right = core.Snake(np.array([6, 6]), 4, core.RIGHT)

        snake_up.move(core.UP)
        snake_down.move(core.UP)
        snake_left.move(core.UP)
        snake_right.move(core.UP)

        pos1 = [np.array(x) for x in [(6, 5), (6, 6), (6, 7), (6, 8)]]
        pos2 = [np.array(x) for x in [(6, 7), (6, 6), (6, 5), (6, 4)]]
        pos3 = [np.array(x) for x in [(6, 5), (6, 6), (7, 6), (8, 6)]]
        pos4 = [np.array(x) for x in [(6, 5), (6, 6), (5, 6), (4, 6)]]

        assert_snake_has_position(snake_up, pos1)
        assert_snake_has_position(snake_down, pos2)
        assert_snake_has_position(snake_left, pos3)
        assert_snake_has_position(snake_right, pos4)

    def test_snake_move_down(self):
        snake_up = core.Snake(np.array([6, 6]), 4, core.UP)
        snake_down = core.Snake(np.array([6, 6]), 4, core.DOWN)
        snake_left = core.Snake(np.array([6, 6]), 4, core.LEFT)
        snake_right = core.Snake(np.array([6, 6]), 4, core.RIGHT)

        snake_up.move(core.DOWN)
        snake_down.move(core.DOWN)
        snake_left.move(core.DOWN)
        snake_right.move(core.DOWN)

        pos1 = [np.array(x) for x in [(6, 5), (6, 6), (6, 7), (6, 8)]]
        pos2 = [np.array(x) for x in [(6, 7), (6, 6), (6, 5), (6, 4)]]
        pos3 = [np.array(x) for x in [(6, 7), (6, 6), (7, 6), (8, 6)]]
        pos4 = [np.array(x) for x in [(6, 7), (6, 6), (5, 6), (4, 6)]]

        assert_snake_has_position(snake_up, pos1)
        assert_snake_has_position(snake_down, pos2)
        assert_snake_has_position(snake_left, pos3)
        assert_snake_has_position(snake_right, pos4)

    def test_snake_move_left(self):
        snake_up = core.Snake(np.array([6, 6]), 4, core.UP)
        snake_down = core.Snake(np.array([6, 6]), 4, core.DOWN)
        snake_left = core.Snake(np.array([6, 6]), 4, core.LEFT)
        snake_right = core.Snake(np.array([6, 6]), 4, core.RIGHT)

        snake_up.move(core.LEFT)
        snake_down.move(core.LEFT)
        snake_left.move(core.LEFT)
        snake_right.move(core.LEFT)

        pos1 = [np.array(x) for x in [(5, 6), (6, 6), (6, 7), (6, 8)]]
        pos2 = [np.array(x) for x in [(5, 6), (6, 6), (6, 5), (6, 4)]]
        pos3 = [np.array(x) for x in [(5, 6), (6, 6), (7, 6), (8, 6)]]
        pos4 = [np.array(x) for x in [(7, 6), (6, 6), (5, 6), (4, 6)]]

        assert_snake_has_position(snake_up, pos1)
        assert_snake_has_position(snake_down, pos2)
        assert_snake_has_position(snake_left, pos3)
        assert_snake_has_position(snake_right, pos4)

    def test_snake_move_right(self):
        snake_up = core.Snake(np.array([6, 6]), 4, core.UP)
        snake_down = core.Snake(np.array([6, 6]), 4, core.DOWN)
        snake_left = core.Snake(np.array([6, 6]), 4, core.LEFT)
        snake_right = core.Snake(np.array([6, 6]), 4, core.RIGHT)

        snake_up.move(core.RIGHT)
        snake_down.move(core.RIGHT)
        snake_left.move(core.RIGHT)
        snake_right.move(core.RIGHT)

        pos1 = [np.array(x) for x in [(7, 6), (6, 6), (6, 7), (6, 8)]]
        pos2 = [np.array(x) for x in [(7, 6), (6, 6), (6, 5), (6, 4)]]
        pos3 = [np.array(x) for x in [(5, 6), (6, 6), (7, 6), (8, 6)]]
        pos4 = [np.array(x) for x in [(7, 6), (6, 6), (5, 6), (4, 6)]]

        assert_snake_has_position(snake_up, pos1)
        assert_snake_has_position(snake_down, pos2)
        assert_snake_has_position(snake_left, pos3)
        assert_snake_has_position(snake_right, pos4)

    def test_single_length_snake_cannot_reverse(self):
        snake = core.Snake(np.array([3, 3]), 1, core.UP)
        snake.move(core.DOWN)

        assert_snake_has_position(snake, [np.array([3, 2])])

    def test_snake_self_intersects(self):
        snake = core.Snake(np.array([3, 3]), 5, core.LEFT)
        self.assertFalse(snake.intersects(snake.head().pos, 1))
        snake.move(core.DOWN)
        self.assertFalse(snake.intersects(snake.head().pos, 1))
        snake.move(core.RIGHT)
        self.assertFalse(snake.intersects(snake.head().pos, 1))
        snake.move(core.UP)
        self.assertTrue(snake.intersects(snake.head().pos, 1))

    def test_state_becomes_unplayable_on_update(self):
        snake = core.Snake(np.array([2, 1]), 3, core.LEFT)
        state = core.GameState(snake, 5, 5)
        self.assertTrue(state.is_playable())
        state.update(core.LEFT)
        self.assertTrue(state.is_playable())
        state.update(core.LEFT)
        self.assertFalse(state.is_playable())

        assert_snake_has_position(snake, [[0, 1], [1, 1], [2, 1]])

    def test_state_matrix_correct(self):
        snake = core.Snake(np.array([5, 5]), 3, core.RIGHT)
        state = core.GameState(snake, 10, 10)

        matrix = state.to_matrix()
        food = state.food()
        self._check_matrix(snake, matrix, food)

    def test_board_does_not_make_changes_after_game_over(self):
        snake = core.Snake(np.array([1, 1]), 1, core.LEFT)
        state = core.GameState(snake, 5, 5)

        self.assertTrue(state.is_playable())
        state.update(core.LEFT)
        self.assertFalse(state.is_playable())
        assert_snake_has_position(snake, [[0, 1]])

        for i in range(10):
            state.update(core.LEFT)

        assert_snake_has_position(snake, [[0, 1]])

    def test_multiple_legal_moves(self):
        snake = core.Snake(np.array([5, 5]), 3, core.LEFT)
        state = core.GameState(snake, 10, 10, 0)

        self.assertTrue(state.is_playable())
        snake.move(core.LEFT)
        self.assertTrue(state.is_playable())
        snake.move(core.UP)
        self.assertTrue(state.is_playable())
        snake.move(core.RIGHT)
        self.assertTrue(state.is_playable())
        snake.move(core.UP)
        self.assertTrue(state.is_playable())

        assert_snake_has_position(snake, [[5, 3], [5, 4], [4, 4]])

        matrix = state.to_matrix()
        self._check_matrix(snake, matrix)

    def test_high_oob(self):
        snake = core.Snake(np.array([5, 5]), 3, core.RIGHT)
        state = core.GameState(snake, 6, 6, 0)

        self.assertTrue(state.is_playable())
        state.update(core.RIGHT)
        self.assertFalse(state.is_playable())

        snake = core.Snake(np.array([5, 5]), 3, core.RIGHT)
        state = core.GameState(snake, 6, 6, 0)
        state.update(core.DOWN)
        self.assertFalse(state.is_playable())

    def test_snake_grows(self):
        snake = core.Snake(np.array([3, 3]), 2, core.LEFT)
        snake.move(core.LEFT, True)
        snake.move(core.LEFT)
        self.assertEqual(2, len(snake))
        snake.move(core.LEFT)
        self.assertEqual(3, len(snake))

    def test_snake_grows_from_state(self):
        # TODO(matthew-c21): Update this to match any changes to the seeding in GameState.
        snake = core.Snake(np.array([5, 5]), 2, core.LEFT)
        state = core.GameState(snake, 10, 10, seed=10)

        for _ in range(4):
            state.update(core.UP)

        for _ in range(2):
            state.update(core.LEFT)

        self.assertEqual(3, len(snake))

    def test_game_state_does_not_degrade_normally(self):
        snake = core.Snake(np.array([5, 5]), 1, core.LEFT)
        state = core.GameState(snake, 10, 10, food_max=0)

        # Execute 1,000 moves to check against a drought.
        for i in range(250):
            state.update(core.DOWN)
            state.update(core.RIGHT)
            state.update(core.UP)
            state.update(core.LEFT)

        self.assertTrue(state.is_playable())

    def test_game_state_becomes_invalid_after_drought(self):
        snake = core.Snake(np.array([5, 5]), 1, core.LEFT)
        state = core.GameState(snake, 10, 10, food_max=0, max_drought=10)

        moves = cycle([core.DOWN, core.RIGHT, core.UP, core.LEFT])
        for _ in range(10):
            move = next(moves)
            state.update(move)
            self.assertTrue(state.is_playable())

        state.update(core.UP)
        self.assertFalse(state.is_playable())

    def test_multiple_food_items(self):
        snake = core.Snake(np.array([5, 5]), 1, core.RIGHT)
        state = core.GameState(snake, 10, 10, food_max=5)

        self.assertEqual(5, len(state.food()))

        state.update(core.RIGHT)
        self.assertEqual(5, len(state.food()))

    def test_food_regenerated_upon_eating(self):
        snake = core.Snake(np.array([5, 5]), 1, core.RIGHT)
        state = core.GameState(snake, 10, 10, seed=10, food_max=5)

        self.assertEqual(5, len(state.food()))

        for _ in range(4):
            state.update(core.UP)

        self.assertEqual(5, len(state.food()))

    def test_setting_food_items_persistent(self):
        snake = core.Snake(np.array([5, 5]), 1, core.RIGHT)
        state = core.GameState(snake, 10, 10, food_max=5)
        food = core._food_item(np.array([6, 5]), 100)

        state.set_food([food])

        self.assertEqual(5, len(state.food()))
        self.assertTrue(any(x is food for x in state.food()))

        state.update(core.RIGHT)

        self.assertTrue(all(x is not food for x in state.food()))
        self.assertEqual(5, len(state.food()))


if __name__ == '__main__':
    unittest.main()
