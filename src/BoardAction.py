import numpy as np

from src import BoardConf as bc
from src.AIManager import ai_player

MAX_MOVEMENTS = 6

board = np.zeros((bc.BOARD_ROWS, bc.BOARD_COLS))
active_player = None
num_of_movement = None
played_obj_pos = None
movement_count = None

def setup_board():
    global board, active_player, played_obj_pos, movement_count, num_of_movement
    active_player = 1
    num_of_movement = 2
    played_obj_pos = (-1, -1)
    movement_count = 0

    board = np.zeros((bc.BOARD_ROWS, bc.BOARD_COLS))

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

def getListOfPos(tmp_board, player):
    pos = []

    for i in range(bc.BOARD_ROWS):
        for j in range(bc.BOARD_COLS):
            if tmp_board[i][j] == player:
                pos.append((i,j))

    return pos

def unselect_obj(pos):
    board[pos[0]][pos[1]] = active_player

def check_pos_empty(pos):
    return board[pos[0]][pos[1]] == 0

def check_movement(tmp_board, source, dest):
    if dest[0] < 0 or dest[0] >= bc.BOARD_ROWS or dest[1] < 0 or dest[1] >= bc.BOARD_COLS:
        return False

    if not ((source[0] == dest[0] or source[1] == dest[1]) and played_obj_pos != source):
        return False

    if tmp_board[dest[0]][dest[1]] != 0:
        return False

    if source[0] == dest[0] and abs(source[1] - dest[1]) == 1:
        return True

    if source[1] == dest[1] and abs(source[0] - dest[0]) == 1:
        return True

    return False

def death(tmp_board, del_list):
    global played_obj_pos, num_of_movement
    for col, row in del_list:
        tmp_board[col][row] = 0

    #todo: fix this part (I thing its wrong)
    if np.count_nonzero(tmp_board == active_player) == 1:
        num_of_movement = 1
        played_obj_pos = (-1, -1)

    return tmp_board

def check_death(tmp_board, row, col, player, init, init_control, del_tmp, board_size):
    del_list = np.empty((0, 2), int)

    if tmp_board[col][row] == (player % 2) + 1 and init_control == init + 1:
        init = init_control
        del_tmp = np.vstack([del_tmp, (col, row)])

    elif tmp_board[col][row] == (player % 2) + 1 and not init_control == init + 1:
        init = -1
        del_tmp = np.empty((0, 2), int)

    elif tmp_board[col][row] == player and del_tmp.size == 0:
        init = init_control
        del_list = np.vstack((del_list, del_tmp))

    elif tmp_board[col][row] == player and del_tmp.size != 0 and init_control == init + 1:
        init = init_control
        del_list = np.vstack((del_list, del_tmp))
        del_tmp = np.empty((0, 2), int)

    if init == board_size - 1:
        del_list = np.vstack((del_list, del_tmp))

    return del_list, del_tmp, init

def control_death(tmp_board, pos):

    del_list = np.empty((0, 2), int)
    del_tmp_1 = np.empty((0, 2), int)
    del_tmp_2 = np.empty((0, 2), int)

    # Control in row

    row = pos[1]
    init_1, init_2 = -1, -1

    for col in range(bc.BOARD_COLS):
        del_l, del_tmp_1, init_1 = check_death(tmp_board, row, col, 1, init_1, col, del_tmp_1, bc.BOARD_COLS)
        del_list = np.vstack((del_list, del_l))

        del_l, del_tmp_2, init_2 = check_death(tmp_board, row, col, 2, init_2, col, del_tmp_2, bc.BOARD_COLS)
        del_list = np.vstack((del_list, del_l))

    del_tmp_1 = np.empty((0, 2), int)
    del_tmp_2 = np.empty((0, 2), int)

    # Control in col

    col = pos[0]
    init_1, init_2 = -1, -1

    for row in range(bc.BOARD_ROWS):
        del_l, del_tmp_1, init_1 = check_death(tmp_board, row, col, 1, init_1, row, del_tmp_1, bc.BOARD_ROWS)
        del_list = np.vstack((del_list, del_l))

        del_l, del_tmp_2, init_2 = check_death(tmp_board, row, col, 2, init_2, row, del_tmp_2, bc.BOARD_ROWS)
        del_list = np.vstack((del_list, del_l))

    death(tmp_board, del_list)

def control_win_cond(tmp_board):
    p1_count = np.count_nonzero(tmp_board == 1)
    p2_count = np.count_nonzero(tmp_board == 2)

    if movement_count == MAX_MOVEMENTS:
        if p1_count == p2_count:
            return 0

        if p1_count > p2_count:
            return 1

        else:
            return 2


    if (p1_count == 0 and p2_count == 0) or (p1_count == 1 and p2_count == 1):
        return 0

    if p1_count == 0:
        return 2

    if p2_count == 0:
        return 1

    return -1

def move(tmp_board, player, source, dest):
    global active_player, num_of_movement, played_obj_pos, movement_count

    if player != active_player:
        return tmp_board

    if check_movement(tmp_board, source, dest):
        tmp_board[dest[0]][dest[1]] = tmp_board[source[0]][source[1]] / 3
        tmp_board[source[0]][source[1]] = 0

        if active_player == ai_player:
            tmp_board[dest[0]][dest[1]] = player

        played_obj_pos = dest
        num_of_movement -= 1

        if num_of_movement == 0:
            active_player = player % 2 + 1
            num_of_movement = get_movement_count()
            played_obj_pos = (-1, -1)

        movement_count += 1
        control_death(tmp_board, dest)

    return tmp_board