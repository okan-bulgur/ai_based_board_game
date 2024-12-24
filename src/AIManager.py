import multiprocessing
import time

from src import BoardAction as b_act
import numpy as np
import random

directions = [(-1,0), (1,0), (0,-1), (0,1)]
ai_player = 1
opponent_player = ai_player % 2 + 1

def calculate_piece_count_factor(state, aggressivity=1):
    p1_count = np.count_nonzero(state.get_board() == ai_player)
    p2_count = np.count_nonzero(state.get_board() == opponent_player)

    return p1_count - (aggressivity * p2_count) # I want to kill as many pieces as I can

def calculate_mobility_factor(state):
    positions_1 = b_act.get_list_of_pos(state.get_board(), ai_player)
    positions_2 = b_act.get_list_of_pos(state.get_board(), opponent_player)
    count_1 = 0
    count_2 = 0

    for dir in directions:
        for pos in positions_1:
            dest = tuple(p + d for p, d in zip(pos, dir))
            if b_act.check_movement(state, pos, dest):
                count_1 += 1

        for pos in positions_2:
            dest = tuple(p + d for p, d in zip(pos, dir))
            if b_act.check_movement(state, pos, dest):
                count_2 += 1

    return count_1 - count_2

def calculate_count_of_center_factor(state):
    center_board = state.get_board()[2:5, 2:5]
    p1_count_center = np.count_nonzero(center_board == ai_player)
    p2_count_center = np.count_nonzero(center_board == opponent_player)

    return p1_count_center - p2_count_center

def calculate_count_of_corner_factor(state):
    corners = [(1, 1), (1, 5), (5, 1), (5, 5)]
    player_1 = sum(1 for corner in corners if state.get_value_of_board(corner[0], corner[1]) == ai_player)
    player_2 = sum(1 for corner in corners if state.get_value_of_board(corner[0], corner[1]) == opponent_player)

    return player_1 - player_2

def evaluation(state):
    score = 20 * calculate_piece_count_factor(state, 2)
    score += 10 * calculate_mobility_factor(state)
    score += 5 * calculate_count_of_center_factor(state)
    score += 3 * calculate_count_of_corner_factor(state)

    return score

def get_point(state):
    cond = b_act.control_win_cond(state)
    eval_point = evaluation(state)

    if cond == 0:
        return eval_point
    elif cond == ai_player:
        return 10000 + eval_point
    elif cond == opponent_player:
        return -10000 + eval_point

    return None

def evaluate_move(args):
    pos, dir, state = args
    dest = tuple(p + d for p, d in zip(pos, dir))
    if b_act.check_movement(state, pos, dest):
        state_copy = state.__copy__()
        b_act.move(state_copy, ai_player, pos, dest, True)
        score = minimax(state_copy, True)
        return score, pos, dest
    return None, None, None

def play():
    start_time = time.time()
    state_copy = b_act.state.__copy__()
    positions = b_act.get_list_of_pos(state_copy.get_board(), ai_player)

    best_score = float("-inf")
    move_source = (-1, -1)
    move_dest = (-1, -1)

    random.shuffle(directions)
    tasks = [(pos, dir, state_copy) for pos in positions for dir in directions]

    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(evaluate_move, tasks)

    for result in results:
        if result[0] is not None and result[0] > best_score:
            print("result:", result)
            best_score = result[0]
            move_source = result[1]
            move_dest = result[2]

    if move_dest != (-1, -1):
        b_act.move(b_act.state, ai_player, move_source, move_dest, True)
        print("Time:", time.time() - start_time)

def minimax(state, is_max, alpha=float("-inf"), beta=float("inf"), depth=0):
    point = get_point(state)
    if point is not None:
        return point

    if depth == 4:
        return evaluation(state)

    if is_max:
        best_score = float("-inf")
        positions = b_act.get_list_of_pos(state.get_board(), ai_player)

        for pos1 in positions:
            for dir1 in directions:
                dest1 = tuple(p + d for p, d in zip(pos1, dir1))

                if b_act.check_movement(state, pos1, dest1):
                    state_copy_1 = state.__copy__()
                    b_act.move(state_copy_1, ai_player, pos1, dest1, True)

                    point = get_point(state_copy_1)
                    if point is not None:
                        return point

                    positions_after_first = b_act.get_list_of_pos(state_copy_1.get_board(), ai_player)
                    for pos2 in positions_after_first:
                        for dir2 in directions:
                            dest2 = tuple(p + d for p, d in zip(pos2, dir2))
                            if b_act.check_movement(state_copy_1, pos2, dest2):

                                state_copy_2 = state_copy_1.__copy__()
                                b_act.move(state_copy_2, ai_player, pos2, dest2, True)

                                score = minimax(state_copy_2, not is_max, alpha, beta, depth + 2)

                                best_score = max(best_score, score)
                                alpha = max(alpha, best_score)

                                if alpha >= beta:
                                    return best_score
        return best_score

    else:
        best_score = float("inf")
        positions = b_act.get_list_of_pos(state.get_board(), opponent_player)

        for pos1 in positions:
            for dir1 in directions:
                dest1 = tuple(p + d for p, d in zip(pos1, dir1))
                if b_act.check_movement(state, pos1, dest1):

                    state_copy_1 = state.__copy__()
                    b_act.move(state_copy_1, opponent_player, pos1, dest1, True)

                    point = get_point(state_copy_1)
                    if point is not None:
                        return point

                    positions_after_first = b_act.get_list_of_pos(state_copy_1.get_board(), opponent_player)
                    for pos2 in positions_after_first:
                        for dir2 in directions:
                            dest2 = tuple(p + d for p, d in zip(pos2, dir2))
                            if b_act.check_movement(state_copy_1, pos2, dest2):

                                state_copy_2 = state_copy_1.__copy__()
                                b_act.move(state_copy_2, opponent_player, pos2, dest2, True)

                                score = minimax(state_copy_2, not is_max, alpha, beta, depth + 2)

                                best_score = min(best_score, score)
                                beta = min(beta, best_score)

                                if alpha >= beta:
                                    return best_score
        return best_score