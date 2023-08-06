"""
Implements a function to test a strategy for the 2048.
"""
from .cp2048 import Game2048, GameOverException


def evaluate_strategy(fct_strategy, ntries=10):
    for i in range(0, ntries):
        g = Game2048()
        while True:
            try:
                g.next_turn()
            except (GameOverException, RuntimeError):
                break
            d = fct_strategy(g.game, g.state, g.moves)
            g.play(d)
        yield g.score()
