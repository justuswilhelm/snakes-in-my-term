#!/usr/bin/env python3
from curses import (
    error,
    wrapper,
    curs_set,
)
from functools import lru_cache
from time import sleep

from game import (
    make_game_state,
    update_game_state,
)

from game.food import (
    draw_food,
    make_food,
)
from game.player import (
    draw_player,
    update_player,
)

FRAME_DURATION = 0.2


def get_input(stdscr):
    key_mask = ["KEY_UP", "KEY_DOWN", "KEY_RIGHT", "KEY_LEFT"]
    try:
        key = stdscr.getkey()
    except error:
        key = None
    if key in key_mask:
        return key


@lru_cache()
def gen_field(x, y):
    def gen_row(row):
        if row == 0 or row == y - 1:
            return "+" + "-" * (x - 2) + "+"
        else:
            return "|" + " " * (x - 2) + "|"
    return [gen_row(row) for row in range(y)]


def draw_field(field, stdscr):
    for y, row in enumerate(field):
        stdscr.addstr(y, 0, row)


def game_loop(stdscr, game_state):
    y, x = stdscr.getmaxyx()
    y -= 1
    x -= 1
    if not game_state:
        game_state = make_game_state(x, y)
    while True:
        stdscr.clear()
        if not game_state.food:
            game_state.food = make_food(x, y)
        player_state, food = update_player(
            game_state.player_state,
            get_input(stdscr),
            x, y,
            game_state.food)
        if not player_state:
            break

        game_state = update_game_state(game_state, player_state, food)
        draw_field(gen_field(x, y), stdscr)
        draw_food(food, stdscr)
        draw_player(player_state, stdscr)

        stdscr.addstr(0, 5, "Your Score: {}".format(len(player_state.tail)))
        stdscr.refresh()

        sleep(FRAME_DURATION)


def main(stdscr):
    stdscr.nodelay(1)  # Do not block on getch
    curs_set(0)
    try:
        game_loop(
            stdscr,
            None,
        )
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    wrapper(main)

    print("Game Over")
