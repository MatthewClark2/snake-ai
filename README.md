# AI Snake

Use deep Q-learning to train a model to play the game snake. Projects of this scale quickly remind me of why I hate
Python for substantial projects.

#### About Positions and Directions

The game is given as a grid where the upper left corner is `(0, 0)`. Elements are access by `(x, y)` positions,
corresponding to column, row positions.

## Rules

1. The snake may not move into a self-intersecting position.
2. The snake does not grow immediately upon eating. Rather, the tail must reach the position where the food was eaten
before it actually grows.
3. By default, the snake dies when it hits a wall.
4. Food is removed instantly once the snake makes contact with it.

## Running

The main method for the text based game is, fittingly enough, located in `snake_ai/text_game.py`. A version with real
graphical rendering may be done with `pygame` at a later time.

## Tests

All tests are found in the `test` directory. [Nose](https://nose.readthedocs.io/en/latest/) is probably the best way to
go about running them, but any testing framework capable of running Python's standard unit tests should work.
