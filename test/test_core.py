import unittest
import numpy as np
import snake_ai.core as core

def assert_snake_has_position(snake, position):
    for i, part in enumerate(snake):
        np.testing.assert_array_equal(part.position, position[i])


class CoreTest(unittest.TestCase):
    def test_snake_creation_up(self):
        pos = [np.array(x) for x in [(5, 5), (5, 4), (5, 3)]]
        snake = core.Snake(pos[0], 3, core.UP)
        assert_snake_has_position(snake, pos)


    def test_snake_creation_down(self):
        pos = [np.array(x) for x in [(5, 5), (5, 6), (5, 7)]]
        snake = core.Snake(pos[0], 3, core.DOWN)
        (assert_snake_has_position(snake, pos))


    def test_snake_creation_left(self):
        pos = [np.array(x) for x in [(5, 5), (6, 5), (7, 5)]]
        snake = core.Snake(pos[0], 3, core.LEFT)
        (assert_snake_has_position(snake, pos))


    def test_snake_creation_right(self):
        pos = [np.array(x) for x in [(5, 5), (4, 5), (3, 5)]]
        snake = core.Snake(pos[0], 3, core.RIGHT)
        (assert_snake_has_position(snake, pos))


    def test_snake_move_up(self):
        snake_up    = core.Snake(np.array([6, 6]), 4, core.UP)
        snake_down  = core.Snake(np.array([6, 6]), 4, core.DOWN)
        snake_left  = core.Snake(np.array([6, 6]), 4, core.LEFT)
        snake_right = core.Snake(np.array([6, 6]), 4, core.RIGHT)

        snake_up.move(core.UP)
        snake_down.move(core.UP)
        snake_left.move(core.UP)
        snake_right.move(core.UP)

        pos1 = [np.array(x) for x in [(6, 7), (6, 6), (6, 5), (6, 4)]]
        pos2 = [np.array(x) for x in [(6, 5), (6, 6), (6, 7), (6, 8)]]
        pos3 = [np.array(x) for x in [(6, 7), (6, 6), (7, 6), (8, 6)]]
        pos4 = [np.array(x) for x in [(6, 7), (6, 6), (5, 6), (4, 6)]]

        (assert_snake_has_position(snake_up, pos1))
        (assert_snake_has_position(snake_down, pos2))
        (assert_snake_has_position(snake_left, pos3))
        (assert_snake_has_position(snake_right, pos4))


    def test_snake_move_down(self):
        snake_up    = core.Snake(np.array([6, 6]), 4, core.UP)
        snake_down  = core.Snake(np.array([6, 6]), 4, core.DOWN)
        snake_left  = core.Snake(np.array([6, 6]), 4, core.LEFT)
        snake_right = core.Snake(np.array([6, 6]), 4, core.RIGHT)

        snake_up.move(core.DOWN)
        snake_down.move(core.DOWN)
        snake_left.move(core.DOWN)
        snake_right.move(core.DOWN)

        pos1 = [np.array(x) for x in [(6, 7), (6, 6), (6, 5), (6, 4)]]
        pos2 = [np.array(x) for x in [(6, 5), (6, 6), (6, 7), (6, 8)]]
        pos3 = [np.array(x) for x in [(6, 5), (6, 6), (7, 6), (8, 6)]]
        pos4 = [np.array(x) for x in [(6, 5), (6, 6), (5, 6), (4, 6)]]

        (assert_snake_has_position(snake_up, pos1))
        (assert_snake_has_position(snake_down, pos2))
        (assert_snake_has_position(snake_left, pos3))
        (assert_snake_has_position(snake_right, pos4))


    def test_snake_move_left(self):
        snake_up    = core.Snake(np.array([6, 6]), 4, core.UP)
        snake_down  = core.Snake(np.array([6, 6]), 4, core.DOWN)
        snake_left  = core.Snake(np.array([6, 6]), 4, core.LEFT)
        snake_right = core.Snake(np.array([6, 6]), 4, core.RIGHT)

        snake_up.move(core.LEFT)
        snake_down.move(core.LEFT)
        snake_left.move(core.LEFT)
        snake_right.move(core.LEFT)

        pos1 = [np.array(x) for x in [(5, 6), (6, 6), (6, 5), (6, 4)]]
        pos2 = [np.array(x) for x in [(5, 6), (6, 6), (6, 7), (6, 8)]]
        pos3 = [np.array(x) for x in [(5, 6), (6, 6), (7, 6), (8, 6)]]
        pos4 = [np.array(x) for x in [(7, 6), (6, 6), (5, 6), (4, 6)]]

        (assert_snake_has_position(snake_up, pos1))
        (assert_snake_has_position(snake_down, pos2))
        (assert_snake_has_position(snake_left, pos3))
        (assert_snake_has_position(snake_right, pos4))


    def test_snake_move_right(self):
        snake_up    = core.Snake(np.array([6, 6]), 4, core.UP)
        snake_down  = core.Snake(np.array([6, 6]), 4, core.DOWN)
        snake_left  = core.Snake(np.array([6, 6]), 4, core.LEFT)
        snake_right = core.Snake(np.array([6, 6]), 4, core.RIGHT)

        snake_up.move(core.RIGHT)
        snake_down.move(core.RIGHT)
        snake_left.move(core.RIGHT)
        snake_right.move(core.RIGHT)

        pos1 = [np.array(x) for x in [(7, 6), (6, 6), (6, 5), (6, 4)]]
        pos2 = [np.array(x) for x in [(7, 6), (6, 6), (6, 7), (6, 8)]]
        pos3 = [np.array(x) for x in [(5, 6), (6, 6), (7, 6), (8, 6)]]
        pos4 = [np.array(x) for x in [(7, 6), (6, 6), (5, 6), (4, 6)]]

        (assert_snake_has_position(snake_up, pos1))
        (assert_snake_has_position(snake_down, pos2))
        (assert_snake_has_position(snake_left, pos3))
        (assert_snake_has_position(snake_right, pos4))


    def test_single_length_snake_cannot_reverse(self):
        snake = core.Snake(np.array([3, 3]), 1, core.UP)
        snake.move(core.DOWN)

        (assert_snake_has_position(snake, [np.array([3, 4])]))


if __name__ == '__main__':
    unittest.main()
