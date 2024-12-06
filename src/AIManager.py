from src import BoardAction as b_act
import copy

directions = [(-1,0), (1,0), (0,-1), (0,1)]
ai_player = 1
opponent_player = ai_player % 2 + 1

count = 0

def play():
    state_copy = copy.deepcopy(b_act.state)
    positions = b_act.get_list_of_pos(state_copy["board"], ai_player)

    best_score = float("-inf")
    move_source = (-1, -1)
    move_dest = (-1, -1)

    for pos in positions:
        for dir in directions:
            dest = tuple(p + d for p, d in zip(pos, dir))
            if b_act.check_movement(state_copy, pos, dest):

                state_copy_1 = copy.deepcopy(state_copy)
                b_act.move(state_copy_1, ai_player, pos, dest)

                score = minmax(state_copy_1, True)

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
    cond = b_act.control_win_cond(state)
    if cond != -1:
        return cond

    if is_max:
        best_score = float("-inf")
        positions = b_act.get_list_of_pos(state["board"], ai_player)

        for pos1 in positions:
            for dir1 in directions:
                dest1 = tuple(p + d for p, d in zip(pos1, dir1))

                if b_act.check_movement(state, pos1, dest1):
                    state_copy_1 = copy.deepcopy(state)
                    b_act.move(state_copy_1, ai_player, pos1, dest1)

                    cond = b_act.control_win_cond(state_copy_1)
                    if cond != -1:
                        return cond

                    positions_after_first = b_act.get_list_of_pos(state_copy_1["board"], ai_player)
                    for pos2 in positions_after_first:
                        for dir2 in directions:
                            dest2 = tuple(p + d for p, d in zip(pos2, dir2))
                            if b_act.check_movement(state_copy_1, pos2, dest2):

                                state_copy_2 = copy.deepcopy(state_copy_1)
                                b_act.move(state_copy_2, ai_player, pos2, dest2)

                                score = minmax(state_copy_2, not is_max, alpha, beta, depth + 2)

                                best_score = max(best_score, score)
                                alpha = max(alpha, best_score)

                                if alpha >= beta:
                                    return best_score

        return best_score

    else:
        best_score = float("inf")
        positions = b_act.get_list_of_pos(state["board"], opponent_player)

        for pos1 in positions:
            for dir1 in directions:
                dest1 = tuple(p + d for p, d in zip(pos1, dir1))
                if b_act.check_movement(state, pos1, dest1):

                    state_copy_1 = copy.deepcopy(state)
                    b_act.move(state_copy_1, opponent_player, pos1, dest1)

                    cond = b_act.control_win_cond(state_copy_1)
                    if cond != -1:
                        return cond

                    positions_after_first = b_act.get_list_of_pos(state_copy_1["board"], opponent_player)
                    for pos2 in positions_after_first:
                        for dir2 in directions:
                            dest2 = tuple(p + d for p, d in zip(pos2, dir2))
                            if b_act.check_movement(state_copy_1, pos2, dest2):

                                state_copy_2 = copy.deepcopy(state_copy_1)
                                b_act.move(state_copy_2, opponent_player, pos2, dest2)

                                score = minmax(state_copy_2, not is_max, alpha, beta, depth + 2)

                                best_score = max(best_score, score)
                                beta = min(beta, best_score)

                                if alpha >= beta:
                                    return best_score

        return best_score

