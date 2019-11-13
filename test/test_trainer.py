import unittest
import numpy as np
import snake_ai.trainer as trainer
import snake_ai.core as core


class TrainerTest(unittest.TestCase):
    def test_rewards_eating(self):
        # Recall the 10 seed from test_core.
        snake = core.Snake(np.array([5, 5]), 2, core.LEFT)
        state = core.GameState(snake, 10, 10, seed=10)

        has_eaten = False

        for _ in range(4):
            has_eaten = state.update(core.UP)

        actual_reward = trainer.determine_reward(state.is_playable(), 0, has_eaten)
        self.assertLess(0, actual_reward)

    def test_punishes_game_over(self):
        snake = core.Snake(np.array([5, 5]), 2, core.LEFT)
        state = core.GameState(snake, 10, 10)

        for _ in range(4):
            state.update(core.UP)

        state.update(core.UP)

        self.assertFalse(state.is_playable())
        self.assertGreaterEqual(-1, trainer.determine_reward(False, state.is_playable(), False))

    def test_not_eating_gives_negative_distance(self):
        snake = core.Snake(np.array([5, 5]), 2, core.LEFT)
        state = core.GameState(snake, 10, 10, seed=10)

        old_state = state.to_matrix()
        state.update(core.UP)
        new_state = state.to_matrix()

        # snake at (5, 4). Food at (5, 1).
        self.assertEqual(-3.0, trainer.determine_reward(True, state.min_distance_to_food(), False))

    def test_punish_self_intersection(self):
        snake = core.Snake(np.array([5, 5]), 5, core.LEFT)
        state = core.GameState(snake, 10, 10)

        state.update(core.DOWN)
        state.update(core.RIGHT)

        old_state = state.to_matrix()
        state.update(core.UP)
        new_state = state.to_matrix()

        self.assertGreaterEqual(-1, trainer.determine_reward(state.is_playable(), 0, False))

    def test_move_conversion_up(self):
        move = core.UP

        np.testing.assert_array_equal(core.UP, trainer.to_move(0, move))
        np.testing.assert_array_equal(core.LEFT, trainer.to_move(1, move))
        np.testing.assert_array_equal(core.RIGHT, trainer.to_move(2, move))

    def test_move_conversion_down(self):
        move = core.DOWN

        np.testing.assert_array_equal(core.DOWN, trainer.to_move(0, move))
        np.testing.assert_array_equal(core.RIGHT, trainer.to_move(1, move))
        np.testing.assert_array_equal(core.LEFT, trainer.to_move(2, move))

    def test_move_conversion_left(self):
        move = core.LEFT

        np.testing.assert_array_equal(core.LEFT, trainer.to_move(0, move))
        np.testing.assert_array_equal(core.DOWN, trainer.to_move(1, move))
        np.testing.assert_array_equal(core.UP, trainer.to_move(2, move))

    def test_move_conversion_right(self):
        move = core.RIGHT

        np.testing.assert_array_equal(core.RIGHT, trainer.to_move(0, move))
        np.testing.assert_array_equal(core.UP, trainer.to_move(1, move))
        np.testing.assert_array_equal(core.DOWN, trainer.to_move(2, move))

    def test_move_conversion_oob(self):
        self.assertIsNone(trainer.to_move(3, core.UP))
