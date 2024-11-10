import numpy as np
import random

from src import BoardConf as bc

board = np.zeros((bc.BOARD_ROWS, bc.BOARD_COLS))
active_player = 0
num_of_movement = 2

def setup_board():
    global active_player
    active_player = random.randint(1, 2)

    board[0][0] = 1
    board[0][2] = 1
    board[6][4] = 1
    board[6][6] = 1

    board[6][0] = 2
    board[6][2] = 2
    board[0][4] = 2
    board[0][6] = 2

def get_movement_count():
    return 2 if np.count_nonzero(board == active_player) > 1 else 1

def unselect_obj(pos):
    board[pos[0]][pos[1]] = active_player

def check_pos_empty(pos):
    return board[pos[0]][pos[1]] == 0

def check_movement(source, dest):
    return source[0] == dest[0] or source[1] == dest[1]

def move(source, dest):
    global active_player, num_of_movement

    if check_movement(source, dest):
        board[dest[0]][dest[1]] = board[source[0]][source[1]] / 3
        board[source[0]][source[1]] = 0

        num_of_movement -= 1

        if num_of_movement == 0:
            active_player = active_player % 2 + 1
            num_of_movement = get_movement_count()

        return True

    return False