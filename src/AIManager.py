from src import BoardAction as b_act
import numpy as np

directions = [(-1,0), (1,0), (0,-1), (0,1)]
ai_player = 1
opponent_player = ai_player % 2 + 1

count = 0

def evaluation(state):
    p1_count = np.count_nonzero(state.get_board() == ai_player)
    p2_count = np.count_nonzero(state.get_board() == opponent_player)

    return p1_count - p2_count

def get_point(state):
    cond = b_act.control_win_cond(state)
    eval_point = evaluation(state)

    if cond == 0:
        return 0 + eval_point
    elif cond == ai_player:
        return 10 + eval_point
    elif cond == opponent_player:
        return -10 + eval_point

    return None

def play():
    state_copy = b_act.state.__copy__()
    positions = b_act.get_list_of_pos(state_copy.get_board(), ai_player)

    best_score = float("-inf")
    move_source = (-1, -1)
    move_dest = (-1, -1)

    for pos in positions:
        for dir in directions:
            dest = tuple(p + d for p, d in zip(pos, dir))
            print("Pos: ", pos ," Dest:", dest)
            if b_act.check_movement(state_copy, pos, dest):

                state_copy_1 = state_copy.__copy__()
                b_act.move(state_copy_1, ai_player, pos, dest)

                score = minmax(state_copy_1, True)
                print("Score: ", score)

                if score > best_score:
                    best_score = score
                    move_source = pos
                    move_dest = dest

    if move_dest != (-1, -1):
        print("Count:", count)
        b_act.move(b_act.state, ai_player, move_source, move_dest)

def minmax(state, is_max, alpha=float("-inf"), beta=float("inf"), depth=0):
    global count
    count += 1

    point = get_point(state)
    if point is not None:
        return point

    if is_max:
        best_score = float("-inf")
        positions = b_act.get_list_of_pos(state.get_board(), ai_player)

        for pos1 in positions:
            for dir1 in directions:
                dest1 = tuple(p + d for p, d in zip(pos1, dir1))

                if b_act.check_movement(state, pos1, dest1):
                    state_copy_1 = state.__copy__()
                    b_act.move(state_copy_1, ai_player, pos1, dest1)

                    point = get_point(state_copy_1)
                    if point is not None:
                        return point

                    positions_after_first = b_act.get_list_of_pos(state_copy_1.get_board(), ai_player)
                    for pos2 in positions_after_first:
                        for dir2 in directions:
                            dest2 = tuple(p + d for p, d in zip(pos2, dir2))
                            if b_act.check_movement(state_copy_1, pos2, dest2):

                                state_copy_2 = state_copy_1.__copy__()
                                b_act.move(state_copy_2, ai_player, pos2, dest2)

                                score = minmax(state_copy_2, not is_max, alpha, beta, depth + 2)

                                best_score = max(best_score, score)
                                alpha = max(alpha, best_score)

                                if alpha >= beta:
                                    print("1) Pruning alpha: ", alpha, " beta: ", beta)
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
                    b_act.move(state_copy_1, opponent_player, pos1, dest1)

                    point = get_point(state_copy_1)
                    if point is not None:
                        return point

                    positions_after_first = b_act.get_list_of_pos(state_copy_1.get_board(), opponent_player)
                    for pos2 in positions_after_first:
                        for dir2 in directions:
                            dest2 = tuple(p + d for p, d in zip(pos2, dir2))
                            if b_act.check_movement(state_copy_1, pos2, dest2):

                                state_copy_2 = state_copy_1.__copy__()
                                b_act.move(state_copy_2, opponent_player, pos2, dest2)

                                score = minmax(state_copy_2, not is_max, alpha, beta, depth + 2)

                                best_score = min(best_score, score)
                                beta = min(beta, best_score)

                                if alpha >= beta:
                                    print("2) Pruning alpha: ", alpha, " beta: ", beta)
                                    return best_score

        return best_score

