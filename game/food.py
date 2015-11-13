from random import randint

from collections import namedtuple

from game.point import Point


Food = namedtuple('Food', ['pos'])


def make_food(maxx, maxy):
    """
    >>> make_food(10, 10)
    Food(...)
    """
    return Food(Point(randint(1, maxx - 2), randint(1, maxy - 2)))


def draw_food(food, stdscr):
    stdscr.addch(food.pos.y, food.pos.x, "#")
