"""
Implements a strategy for the game 2048.
"""

from .cp2048 import Game2048
import numpy

# On crée une grille avec des poids rangés en serpentin.
weight_grid = numpy.array([[1,10,100,1000],[10000000,1000000,100000,10000],[100000000,1000000000,10000000000,100000000000],[1000000000000000,100000000000000,10000000000000,1000000000000]], dtype=int)

# Produit scalaire canonique de grid avec weight_grid qui va nous permettre de comparer les différentes directions.
# Plus le produit scalaire est élevé, plus la nouvelle grille obtenue aura ses valeurs rangées selon les poids.
def grid_score(grid):
    result = 0
    for i in range(4):
        for j in range(4):
            result += grid[i,j]*weight_grid[i,j]
    return result

# Test d'égalité entre deux tableaux.
def not_equal(a,b):
    for i in range(4):
        for j in range(4):
            if a[i,j] != b[i,j]:
                return True
    return False

def strategy(game, state, moves):
    n = 2 # Nombre de coups d'avance considérée (n=2 a été choisi par compromis entre temps d'exécution et efficacité de la stratégie).
    test_game = Game2048()
    grids = [[game, 0]]
    direction = -1
    for k in range(n):
         # Calcul de toutes les possibilités de grille après n coups joués.
        temp = []
        m = len(grids)
        for j in range(m):
            for i in {0,2,3}:
                temp_dir = i if k == 0 else grids[j][1]
                test_game.game = grids[j][0]
                test_game.play(i)
                if test_game.gameover() and test_game.score() == 2048:
                    direction = temp_dir
                elif not(test_game.gameover()) and not_equal(test_game.game, grids[j][0]):
                    test_game.next_turn()
                    temp.append([test_game.game,temp_dir])
        grids = temp.copy()
    if len(grids) == 0:
        direction = 0
    elif direction == -1:
        maximum = grid_score(grids[0][0])
        direction = grids[0][1]
        for g in grids[1:]:
            # Recherche de la grille qui a ses coefficients rangés de façon la plus proche des masses dans weight_grid.
            score = grid_score(g[0])
            if score > maximum:
                direction = g[1]
                maximum = score
    return direction
