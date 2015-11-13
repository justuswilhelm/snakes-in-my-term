from collections import namedtuple

from game.food import make_food
from game.point import (
    compare_points,
    Point,
    add_points,
    check_point_bounds,
    UP, DOWN, LEFT, RIGHT,
)

PlayerState = namedtuple('PlayerState', ['pos', 'dir', 'tail', 'tail_queue'])


KEY_MAPPING = {
    None: None,
    False: None,
    'KEY_UP': UP,
    'KEY_DOWN': DOWN,
    'KEY_RIGHT': RIGHT,
    'KEY_LEFT': LEFT,
}


def make_player():
    """
    >>> make_player()
    PlayerState(pos=Point(x=1, y=1), dir=Point(x=1, y=0), \
tail=(), tail_queue=0)
    """
    return PlayerState(Point(1, 1), RIGHT, tuple(), 0)


def move_player(player_state):
    """
    >>> move_player(make_player())
    PlayerState(pos=Point(x=2, y=1), ...)
    """
    last_pos = player_state.pos
    return PlayerState(
        add_points(player_state.pos, player_state.dir), player_state.dir,
        move_tail(player_state.tail, last_pos),
        0
    )


def move_tail(tail, last_pos):
    r"""
    >>> move_tail((Point(x=2, y=1), Point(x=1, y=1)), Point(1, 1))
    (Point(x=1, y=1), Point(x=2, y=1))
    >>> move_tail((Point(x=2, y=1), Point(x=1, y=1),\
    ... Point(x=1, y=2)), Point(1, 1))
    (Point(x=1, y=1), Point(x=2, y=1), Point(x=1, y=1))
    """
    return (last_pos, ) + tail[:-1] if tail else ()


def get_allowed_direction(player_state, new_dir):
    if not player_state.tail:
        return new_dir
    else:
        if player_state.dir in [UP, DOWN]:
            return new_dir if new_dir in [LEFT, RIGHT] else player_state.dir
        if player_state.dir in [LEFT, RIGHT]:
            return new_dir if new_dir in [UP, DOWN] else player_state.dir


def update_direction(player_state, input):
    """
    >>> update_direction(make_player(), 'KEY_UP')
    PlayerState(..., dir=Point(x=0, y=-1), ...)
    >>> update_direction(make_player(), None)
    PlayerState(..., dir=Point(x=1, y=0), ...)
    """
    new_dir = get_allowed_direction(
        player_state,
        KEY_MAPPING[input],
    )
    return PlayerState(
        player_state.pos,
        new_dir,
        player_state.tail,
        player_state.tail_queue,
    ) if input else player_state


def append_tail(player_state, tail_pos):
    """
    >>> a = PlayerState(None, None, (), 1)
    >>> append_tail(a, Point(0, 0))
    PlayerState(..., tail=(Point(x=0, y=0),), tail_queue=0)
    """
    return PlayerState(
        player_state.pos, player_state.dir,
        player_state.tail + (tail_pos, ),
        player_state.tail_queue - 1,
    ) if player_state.tail_queue > 0 else player_state


def enqueue_tail(player_state):
    """
    >>> enqueue_tail(make_player())
    PlayerState(..., tail_queue=1)
    """
    return PlayerState(
        player_state.pos,
        player_state.dir,
        player_state.tail,
        player_state.tail_queue + 1,
    )


def update_player(player_state, input, maxx, maxy, food):
    last_pos = player_state.pos

    player_state = update_direction(
        move_player(player_state), input)

    if not check_point_bounds(player_state.pos, maxx, maxy):
        return None, food

    if compare_points(player_state.pos, food.pos):
        player_state = enqueue_tail(player_state)
        food = make_food(maxx, maxy)
    for tail_piece in player_state.tail:
        if compare_points(player_state.pos, tail_piece):
            return None, food

    player_state = append_tail(player_state, last_pos)

    return player_state, food


def draw_player(player_state, stdscr):
    stdscr.addch(player_state.pos.y, player_state.pos.x, "o")
    for tail_piece in player_state.tail:
        stdscr.addch(tail_piece.y, tail_piece.x, "o")
