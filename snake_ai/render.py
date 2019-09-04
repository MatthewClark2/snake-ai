import core


def main():
    snake = core.Snake(np.array([25, 25]), 5, core.LEFT)
    gs = core.GameState(snake, 50, 50)
