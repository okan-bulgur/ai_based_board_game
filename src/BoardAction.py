import numpy as np

from src import BoardConf as bc

MAX_MOVEMENTS = 50

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

def unselect_obj(pos):
    board[pos[0]][pos[1]] = active_player

def check_pos_empty(pos):
    return board[pos[0]][pos[1]] == 0

def check_movement(source, dest):
    if not ((source[0] == dest[0] or source[1] == dest[1]) and played_obj_pos != source):
        return False

    if board[dest[0]][dest[1]] != 0:
        return False

    if source[0] == dest[0] and abs(source[1] - dest[1]) == 1:
        return True

    if source[1] == dest[1] and abs(source[0] - dest[0]) == 1:
        return True

    return False

def death(del_list):
    global played_obj_pos, num_of_movement

    for col, row in del_list:
        board[col][row] = 0

    #todo: fix this part (I thing its wrong)
    if np.count_nonzero(board == active_player) == 1:
        num_of_movement = 1
        played_obj_pos = (-1, -1)

def check_death(row, col, player, init, init_control, del_tmp, board_size):
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

def control_death(pos):

    del_list = np.empty((0, 2), int)
    del_tmp_1 = np.empty((0, 2), int)
    del_tmp_2 = np.empty((0, 2), int)

    # Control in row

    row = pos[1]
    init_1, init_2 = -1, -1

    for col in range(bc.BOARD_COLS):
        del_l, del_tmp_1, init_1 = check_death(row, col, 1, init_1, col, del_tmp_1, bc.BOARD_COLS)
        del_list = np.vstack((del_list, del_l))

        del_l, del_tmp_2, init_2 = check_death(row, col, 2, init_2, col, del_tmp_2, bc.BOARD_COLS)
        del_list = np.vstack((del_list, del_l))

    del_tmp_1 = np.empty((0, 2), int)
    del_tmp_2 = np.empty((0, 2), int)

    # Control in col

    col = pos[0]
    init_1, init_2 = -1, -1

    for row in range(bc.BOARD_ROWS):
        del_l, del_tmp_1, init_1 = check_death(row, col, 1, init_1, row, del_tmp_1, bc.BOARD_ROWS)
        del_list = np.vstack((del_list, del_l))

        del_l, del_tmp_2, init_2 = check_death(row, col, 2, init_2, row, del_tmp_2, bc.BOARD_ROWS)
        del_list = np.vstack((del_list, del_l))

    death(del_list)

def control_win_cond():
    p1_count = np.count_nonzero(board == 1)
    p2_count = np.count_nonzero(board == 2)

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

def move(source, dest):
    global active_player, num_of_movement, played_obj_pos, movement_count

    if check_movement(source, dest):
        board[dest[0]][dest[1]] = board[source[0]][source[1]] / 3
        board[source[0]][source[1]] = 0

        played_obj_pos = dest
        num_of_movement -= 1

        if num_of_movement == 0:
            active_player = active_player % 2 + 1
            num_of_movement = get_movement_count()
            played_obj_pos = (-1, -1)

        movement_count += 1
        control_death(dest)
        win_cond = control_win_cond()

        if win_cond != -1:
            if win_cond == 0:
                print("DRAW")
            else:
                print("Player 1 won" if win_cond == 1 else "Player 2 won" )

        return win_cond

    return -2