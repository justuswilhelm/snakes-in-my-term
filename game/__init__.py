from collections import namedtuple

from game.player import make_player
from game.food import make_food

GameState = namedtuple('GameState', ['player_state', 'food'])


def make_game_state(maxx, maxy):
    """
    >>> make_game_state(10, 10)
    GameState(player_state=PlayerState(...), food=Food(...))
    """
    return GameState(make_player(), make_food(maxx, maxy))


def update_game_state(game_state, player_state, food):
    return GameState(player_state, food)
