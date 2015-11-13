from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

UP = Point(0, -1)
DOWN = Point(0, 1)
LEFT = Point(-1, 0)
RIGHT = Point(1, 0)


def add_points(a, b):
    """
    >>> a = Point(1, 1)
    >>> b = Point(1, 1)
    >>> add_points(a, b)
    Point(x=2, y=2)
    """
    return Point(a.x + b.x, a.y + b.y)


def compare_points(a, b):
    """
    >>> compare_points(Point(1, 1), Point(1, 1))
    True
    """
    return a.x == b.x and a.y == b.y


def check_point_bounds(point, maxx, maxy):
    """
    Check whether point is in game field bounds.

    >>> check_point_bounds(Point(0, 2), 80, 24)
    False
    >>> check_point_bounds(Point(1, 1), 80, 24)
    True
    """
    return not any([
        point.x < 1,
        point.x > maxx - 2,
        point.y < 1,
        point.y > maxy - 2,
    ])
