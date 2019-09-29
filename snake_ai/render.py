from abc import ABC, abstractmethod

# TODO(matthew-c21): Move all renderers into this file.
# TODO(matthew-c21): Have all renderers show debugging information about the game state rather than just a raw cut of it.

class Renderer(ABC):
    """Showing the game itself requires some level of persistent resources as well as actual rendering logic. This class serves as the basis for all implementations."""
    @abstractmethod
    def render(self, game_state):
        """Render the current game state as is. This method should recycle any resources currently in use by the renderer.

        Arguments
        game_state: the current state to be rendered."""
        pass


    @abstractmethod
    def replay(self, initial_state, moves, food, replay_speed):
        """Given an initial game state and a list of moves, play back the game from start to the point at which moves are no longer given.

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
