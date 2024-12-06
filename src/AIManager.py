from src import BoardAction as b_act
import numpy as np

directions = [(-1,0), (1,0), (0,-1), (0,1)]
ai_player = 1
opponent_player = ai_player % 2 + 1

def play():
    prev_active_player = b_act.active_player
    prev_num_of_movement = b_act.num_of_movement
    prev_played_obj_pos = b_act.played_obj_pos
    prev_movement_count = b_act.movement_count

    board = np.copy(b_act.board)
    positions = b_act.getListOfPos(board, ai_player)

    best_score = float("-inf")
    move_source = (-1, -1)
    move_dest = (-1, -1)

    for pos in positions:
        for dir in directions:
            dest = tuple(p + d for p, d in zip(pos, dir))
            if b_act.check_movement(board, pos, dest):

                copy_board = np.copy(board)
                copy_board = b_act.move(copy_board, ai_player, pos, dest)

                score = minmax(copy_board, True)

                if score > best_score:
                    best_score = score
                    move_source = pos
                    move_dest = dest

    if move_dest != (-1, -1):

        b_act.active_player = prev_active_player
        b_act.num_of_movement = prev_num_of_movement
        b_act.played_obj_pos = prev_played_obj_pos
        b_act.movement_count = prev_movement_count

        b_act.board = b_act.move(b_act.board, ai_player, move_source, move_dest)

def minmax(board, is_max, alpha=float("-inf"), beta=float("inf")):
    cond = b_act.control_win_cond(board)
    if cond != -1:
        return cond

    if is_max:
        best_score = float("-inf")
        positions = b_act.getListOfPos(board, ai_player)

        for pos1 in positions:
            for dir1 in directions:
                dest1 = tuple(p + d for p, d in zip(pos1, dir1))

                if b_act.check_movement(board, pos1, dest1):
                    copy_board_1 = np.copy(board)
                    copy_board_1 = b_act.move(copy_board_1, ai_player, pos1, dest1)

                    cond = b_act.control_win_cond(copy_board_1)
                    if cond != -1:
                        return cond

                    positions_after_first = b_act.getListOfPos(copy_board_1, ai_player)
                    for pos2 in positions_after_first:
                        for dir2 in directions:
                            dest2 = tuple(p + d for p, d in zip(pos2, dir2))
                            if b_act.check_movement(copy_board_1, pos2, dest2):

                                copy_board_2 = np.copy(copy_board_1)
                                copy_board_2 = b_act.move(copy_board_2, ai_player, pos2, dest2)

                                score = minmax(copy_board_2, not is_max, alpha, beta)

                                best_score = max(best_score, score)
                                alpha = max(alpha, best_score)

                                if alpha >= beta:
                                    return best_score

        return best_score

    else:
        best_score = float("inf")
        positions = b_act.getListOfPos(board, opponent_player)

        for pos1 in positions:
            for dir1 in directions:
                dest1 = tuple(p + d for p, d in zip(pos1, dir1))
                if b_act.check_movement(board, pos1, dest1):

                    copy_board_1 = np.copy(board)
                    copy_board_1 = b_act.move(copy_board_1, opponent_player, pos1, dest1)

                    cond = b_act.control_win_cond(copy_board_1)
                    if cond != -1:
                        return cond

                    positions_after_first = b_act.getListOfPos(copy_board_1, opponent_player)
                    for pos2 in positions_after_first:
                        for dir2 in directions:
                            dest2 = tuple(p + d for p, d in zip(pos2, dir2))
                            if b_act.check_movement(copy_board_1, pos2, dest2):

                                copy_board_2 = np.copy(copy_board_1)
                                copy_board_2 = b_act.move(copy_board_2, opponent_player, pos2, dest2)

                                score = minmax(copy_board_2, not is_max, alpha, beta)

                                best_score = max(best_score, score)
                                beta = min(beta, best_score)

                                if alpha >= beta:
                                    return best_score

        return best_score

