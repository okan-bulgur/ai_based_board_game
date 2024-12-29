import numpy as np

from src.Config import BoardConfig as bc
from src.State import State

MAX_MOVEMENTS = 50

state = State(np.zeros((bc.BOARD_ROWS, bc.BOARD_COLS)), 1, 2, 0, (-1, -1))

def setup_state():
    state.set_board(np.zeros((bc.BOARD_ROWS, bc.BOARD_COLS)))
    state.set_active_player(1)
    state.set_num_of_movement(2)
    state.set_movement_count(0)
    state.set_played_obj_pos((-1, -1))

    setup_board()

def setup_board():
    state.get_board()[0][0] = 1
    state.get_board()[0][2] = 1
    state.get_board()[6][4] = 1
    state.get_board()[6][6] = 1

    state.get_board()[6][0] = 2
    state.get_board()[6][2] = 2
    state.get_board()[0][4] = 2
    state.get_board()[0][6] = 2

def get_movement_count(state_cpy):
    return 2 if np.count_nonzero(state_cpy.get_board() == state_cpy.get_active_player()) > 1 else 1

def get_list_of_pos(board, player):
    pos = []

    for i in range(bc.BOARD_ROWS):
        for j in range(bc.BOARD_COLS):
            if board[i][j] == player:
                pos.append((i,j))

    return pos

def unselect_obj(pos):
    state.get_board()[pos[0]][pos[1]] = state.get_active_player()

def check_pos_empty(pos):
    return state.get_board()[pos[0]][pos[1]] == 0

def check_movement(state_cpy, source, dest):
    if state_cpy.get_num_of_movement() == 0:
        return False

    if dest[0] < 0 or dest[0] >= bc.BOARD_ROWS or dest[1] < 0 or dest[1] >= bc.BOARD_COLS:
        return False

    if not ((source[0] == dest[0] or source[1] == dest[1]) and state_cpy.get_played_obj_pos() != source):
        return False

    if state_cpy.get_value_of_board(dest[0], dest[1]) != 0:
        return False

    if source[0] == dest[0] and abs(source[1] - dest[1]) == 1:
        return True

    if source[1] == dest[1] and abs(source[0] - dest[0]) == 1:
        return True

    return False

def death(state_cpy, del_list):
    for col, row in del_list:
        state_cpy.update_board(col, row, 0)

    #todo: fix this part (I thing its wrong)
    if np.count_nonzero(state_cpy.get_board() == state_cpy.get_active_player()) == 1:
        state_cpy.set_num_of_movement(1)
        state_cpy.set_played_obj_pos((-1, -1))

def check_death(board, row, col, player, init, init_control, del_tmp, board_size):
    del_list = np.empty((0, 2), int)

    if board[col][row] == (player % 2) + 1 and init_control == init + 1:
        init = init_control
        del_tmp = np.vstack([del_tmp, (col, row)])

    elif board[col][row] == (player % 2) + 1 and not init_control == init + 1:
        init = -1
        del_tmp = np.empty((0, 2), int)

    elif board[col][row] == player and del_tmp.size == 0:
        init = init_control
        del_list = np.vstack((del_list, del_tmp))

    elif board[col][row] == player and del_tmp.size != 0 and init_control == init + 1:
        init = init_control
        del_list = np.vstack((del_list, del_tmp))
        del_tmp = np.empty((0, 2), int)

    if init == board_size - 1:
        del_list = np.vstack((del_list, del_tmp))

    return del_list, del_tmp, init

def control_death(state_cpy, pos):
    if ((pos[0] - 1 < 0 or state_cpy.get_value_of_board(pos[0] - 1, pos[1]) == 0)
            and (pos[0] + 1 >= bc.BOARD_ROWS or state_cpy.get_value_of_board(pos[0] + 1, pos[1]) == 0)
            and (pos[1] - 1 < 0 or state_cpy.get_value_of_board(pos[0], pos[1] - 1) == 0)
            and (pos[1] + 1 >= bc.BOARD_COLS or state_cpy.get_value_of_board(pos[0], pos[1] + 1) == 0)):
        return

    del_list = np.empty((0, 2), int)
    del_tmp_1 = np.empty((0, 2), int)
    del_tmp_2 = np.empty((0, 2), int)

    # Control in row

    row = pos[1]
    init_1, init_2 = -1, -1

    for col in range(bc.BOARD_COLS):
        del_l, del_tmp_1, init_1 = check_death(state_cpy.get_board(), row, col, 1, init_1, col, del_tmp_1, bc.BOARD_COLS)
        del_list = np.vstack((del_list, del_l))

        del_l, del_tmp_2, init_2 = check_death(state_cpy.get_board(), row, col, 2, init_2, col, del_tmp_2, bc.BOARD_COLS)
        del_list = np.vstack((del_list, del_l))

    del_tmp_1 = np.empty((0, 2), int)
    del_tmp_2 = np.empty((0, 2), int)

    # Control in col

    col = pos[0]
    init_1, init_2 = -1, -1

    for row in range(bc.BOARD_ROWS):
        del_l, del_tmp_1, init_1 = check_death(state_cpy.get_board(), row, col, 1, init_1, row, del_tmp_1, bc.BOARD_ROWS)
        del_list = np.vstack((del_list, del_l))

        del_l, del_tmp_2, init_2 = check_death(state_cpy.get_board(), row, col, 2, init_2, row, del_tmp_2, bc.BOARD_ROWS)
        del_list = np.vstack((del_list, del_l))

    death(state_cpy, del_list)

def control_win_cond(state_cpy):
    p1_count = np.count_nonzero(state_cpy.get_board() == 1)
    p1_count += np.count_nonzero(state_cpy.get_board() == 3)

    p2_count = np.count_nonzero(state_cpy.get_board() == 2)
    p2_count += np.count_nonzero(state_cpy.get_board() == 6)

    if state_cpy.get_movement_count() == MAX_MOVEMENTS:
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

def move(state_cpy, player, source, dest, is_ai_play_mode):

    if player != state_cpy.get_active_player():
        return

    if check_movement(state_cpy, source, dest):
        if is_ai_play_mode:
            state_cpy.update_board(dest[0], dest[1], state_cpy.get_value_of_board(source[0], source[1]))
        else:
            state_cpy.update_board(dest[0], dest[1], state_cpy.get_value_of_board(source[0], source[1]) / 3)

        state_cpy.update_board(source[0], source[1], 0)

        state_cpy.set_played_obj_pos(dest)
        state_cpy.set_num_of_movement(state_cpy.get_num_of_movement() - 1)

        if state_cpy.get_num_of_movement() == 0:
            state_cpy.set_active_player(player % 2 + 1)
            state_cpy.set_num_of_movement(get_movement_count(state_cpy))
            state_cpy.set_played_obj_pos((-1, -1))

        state_cpy.set_movement_count(state_cpy.get_movement_count() + 1)
        control_death(state_cpy, dest)