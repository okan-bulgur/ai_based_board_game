import numpy as np

class State:

    def __init__(self, board, active_player, num_of_movement, movement_count, played_obj_pos):
        self.board = board
        self.active_player = active_player
        self.num_of_movement = num_of_movement
        self.movement_count = movement_count
        self.played_obj_pos = played_obj_pos

    def update_board(self, row, col, value):
        self.board[row][col] = value

    def get_value_of_board(self, row, col):
        return self.board[row][col]

    def get_board(self):
        return self.board

    def get_active_player(self):
        return self.active_player

    def get_num_of_movement(self):
        return self.num_of_movement

    def get_movement_count(self):
        return self.movement_count

    def get_played_obj_pos(self):
        return self.played_obj_pos

    def set_board(self, board):
        self.board = board

    def set_active_player(self, active_player):
        self.active_player = active_player

    def set_num_of_movement(self, num_of_movement):
        self.num_of_movement = num_of_movement

    def set_movement_count(self, movement_count):
        self.movement_count = movement_count

    def set_played_obj_pos(self, played_obj_pos):
        self.played_obj_pos = played_obj_pos

    def __copy__(self):
        return State(np.copy(self.board), self.active_player, self.num_of_movement, self.movement_count, self.played_obj_pos)

