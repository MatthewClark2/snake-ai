import unittest
import numpy as np
import snake_ai.trainer as trainer
import snake_ai.core as core


class TrainerTest(unittest.TestCase):
    def test_rewards_eating(self):
        # Recall the 10 seed from test_core.
        snake = core.Snake(np.array([5, 5]), 2, core.LEFT)
        state = core.GameState(snake, 10, 10, seed=10)

        old_state = None
        new_state = None

        for _ in range(4):
            old_state = state.to_matrix()
            state.update(core.UP)
            new_state = state.to_matrix()

        self.assertLess(0, trainer.determine_reward(old_state, new_state, state.is_playable()))

    def test_punishes_game_over(self):
        snake = core.Snake(np.array([5, 5]), 2, core.LEFT)
        state = core.GameState(snake, 10, 10)

        for _ in range(4):
            state.update(core.UP)

        old_state = state.to_matrix()
        state.update(core.UP)
        new_state = state.to_matrix()

        self.assertFalse(state.is_playable())
        self.assertGreater(-1, trainer.determine_reward(old_state, new_state, state.is_playable()))

    def test_sets_movement_punishment(self):
        snake = core.Snake(np.array([5, 5]), 2, core.LEFT)
        state = core.GameState(snake, 10, 10, seed=10)

        old_state = state.to_matrix()
        state.update(core.UP)
        new_state = state.to_matrix()

        self.assertEqual(0, trainer.determine_reward(old_state, new_state, state.is_playable()))
        self.assertEqual(-1, trainer.determine_reward(old_state, new_state, state.is_playable(), movement_reward=-1))

    def test_punish_self_intersection(self):
        snake = core.Snake(np.array([5, 5]), 5, core.LEFT)
        state = core.GameState(snake, 10, 10)

        state.update(core.DOWN)
        state.update(core.RIGHT)

        old_state = state.to_matrix()
        state.update(core.UP)
        new_state = state.to_matrix()

        self.assertGreater(-1, trainer.determine_reward(old_state, new_state, state.is_playable()))
