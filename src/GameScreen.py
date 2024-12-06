from src.Screen import Screen
from src.Button import Button
from src import ScreenManager as sm
from src import BoardAction as b_act
from src import BoardConf as bc
from src import AIManager as ai

from abc import ABC
import sys
import pygame
import numpy as np

SCREEN_COLOR = (255, 244, 234)
CAPTION = 'AI Based Board Game'

HEADER_POS_Y = 75
HEADER_FONT_SIZE = 70
HEADER_FONT_NAME = 'arialblack'
HEADER_COLOR = (201, 104, 104)

COUNTER_POS_X = 25
COUNTER_POS_Y = 25
COUNTER_FONT_SIZE = 20
COUNTER_FONT_NAME = 'arialblack'
COUNTER_COLOR = (201, 104, 104)

HOME_BTN_SIZE = 50
HOME_BTN_GAP = 70

_selected = False
_selected_pos = None
header = ""
play_mode = -1

class GameScreen(Screen, ABC):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GameScreen, cls).__new__(cls)
        return cls._instance

    def __init__(self, sw=0, sh=0):
        super().__init__(sw, sh)
        self.header_txt = "GAME"
        self.screen = None
        self.home_btn = Button

    def setup_home_btn(self):
        home_img = pygame.image.load('res/home.png').convert_alpha()
        home_img.fill((0, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)
        self.home_btn = Button(self.sw-HOME_BTN_GAP, HOME_BTN_GAP - HOME_BTN_SIZE, HOME_BTN_SIZE, HOME_BTN_SIZE,
                               btn_color=SCREEN_COLOR, icon=home_img)
        self.home_btn.draw(self.screen)

    def find_board_conf(self):
        row_len = bc.BOARD_COLS * bc.SQUARE_SIZE
        col_len = bc.BOARD_ROWS * bc.SQUARE_SIZE

        board_gap_x = (self.sw - row_len) // 2
        board_gap_y = (self.sh - col_len) // 2

        start_x = board_gap_x
        end_x = start_x + row_len

        start_y = self.sh - board_gap_y - col_len
        end_y = start_y + col_len

        return start_x, end_x, start_y, end_y

    def draw_board_line(self):

        start_x, end_x, start_y, end_y = self.find_board_conf()

        for i in range(bc.BOARD_ROWS + 1):
            pos_y = start_y + i * bc.SQUARE_SIZE
            pygame.draw.line(self.screen, bc.BOARD_COLOR, (start_x, pos_y), (end_x, pos_y), bc.LINE_WIDTH)

        for j in range(bc.BOARD_COLS + 1):
            pos_x = start_x + j * bc.SQUARE_SIZE
            pygame.draw.line(self.screen, bc.BOARD_COLOR, (pos_x, start_y), (pos_x, end_y), bc.LINE_WIDTH)

    def draw_circle(self, pos, color):

        if color is None:
            color = bc.CIRCLE_COLOR

        start_x, end_x, start_y, end_y = self.find_board_conf()

        center_x = (bc.SQUARE_SIZE * pos[0]) + (bc.SQUARE_SIZE // 2) + start_x
        center_y = (bc.SQUARE_SIZE * pos[1]) + (bc.SQUARE_SIZE // 2) + start_y

        pygame.draw.circle(self.screen, color, [center_x, center_y], bc.CIRCLE_RAD, 0)

    def draw_triangle(self, pos, color):

        if color is None:
            color = bc.TRIANGLE_COLOR

        start_x, end_x, start_y, end_y = self.find_board_conf()

        start_x += bc.SQUARE_SIZE * pos[0]
        start_y += bc.SQUARE_SIZE * pos[1]

        point_1 = (start_x + bc.TRIANGLE_GAP + (bc.SQUARE_SIZE - 2*bc.TRIANGLE_GAP) // 2,  start_y + bc.TRIANGLE_GAP)
        point_2 = (start_x + bc.TRIANGLE_GAP, start_y + bc.SQUARE_SIZE - bc.TRIANGLE_GAP)
        point_3 = (start_x + bc.SQUARE_SIZE - bc.TRIANGLE_GAP, start_y + bc.SQUARE_SIZE - bc.TRIANGLE_GAP)

        pygame.draw.polygon(self.screen, color,[point_1, point_2, point_3])

    def draw_obj(self, pos, player):
        color = bc.SELECT_COLOR if player > 2.0 else None
        player = player / 3 if player > 2 else player

        if player == 1:
            self.draw_triangle(pos, color)
        elif player == 2:
            self.draw_circle(pos, color)

    def draw_board(self):

        self.draw_board_line()

        for row in range(bc.BOARD_ROWS):
            for col in range(bc.BOARD_COLS):
                self.draw_obj((row, col), b_act.state["board"][row][col])

    def find_clicked_board_pos(self, pos):
        pos_x, pos_y = pos
        start_x, end_x, start_y, end_y = self.find_board_conf()

        if pos_x > end_x or pos_x < start_x or pos_y > end_y or pos_y < start_y:
            return (-1, -1)

        row = (pos_x - start_x) // bc.SQUARE_SIZE
        col = (pos_y - start_y) // bc.SQUARE_SIZE

        return row, col

    def is_selected(self, pos):
        row, col = self.find_clicked_board_pos(pos)

        if row == -1:
            return False

        if b_act.state["board"][row][col] == b_act.state["active_player"]:
            b_act.state["board"][row][col] *= 3
            return True

        if b_act.state["board"][row][col] != b_act.state["active_player"]:
            return False

    def unselect_obj(self):
        global _selected_pos, _selected
        b_act.unselect_obj(_selected_pos)
        _selected = False
        _selected_pos = None
        self.reload_screen()

    def select_obj(self, pos):
        global _selected_pos, _selected

        _selected = self.is_selected(pos)
        _selected_pos = self.find_clicked_board_pos(pos) if _selected else None
        self.reload_screen()

    def update_header(self):
        global _selected_pos, _selected, header, play_mode

        cond = b_act.control_win_cond(b_act.state)

        header = f'Player {b_act.state["active_player"]}\'s turn'

        if cond != -1:
            play_mode = -1
            header = f'Player {cond} WON'
            if cond == 0:
                header = f'DRAW'

        self.reload_screen()
        _selected = False
        _selected_pos = None

    def move_obj(self, source, dest):
        global _selected_pos, _selected, header

        b_act.move(b_act.state, b_act.state["active_player"], source, dest)

        self.update_header()

    def reload_screen(self):
        self.screen.fill(SCREEN_COLOR)

        self.setup_header(self.screen, HEADER_FONT_NAME, HEADER_FONT_SIZE, header, HEADER_COLOR, HEADER_POS_Y)
        self.setup_home_btn()

        #Counter
        counter_text = f'Number of movements: {b_act.state["movement_count"]}'
        header_font = pygame.font.SysFont(COUNTER_FONT_NAME, COUNTER_FONT_SIZE)
        res = header_font.render(counter_text, True, COUNTER_COLOR)
        self.screen.blit(res, (COUNTER_POS_X, COUNTER_POS_Y))

        self.draw_board()

    def setup(self):
        global header, play_mode

        pygame.init()

        self.screen = pygame.display.set_mode((self.sw, self.sh))
        self.screen.fill(SCREEN_COLOR)
        pygame.display.set_caption(CAPTION)

        self.setup_header(self.screen, HEADER_FONT_NAME, HEADER_FONT_SIZE, self.header_txt, HEADER_COLOR, HEADER_POS_Y)
        self.setup_home_btn()

        b_act.setup_board()

        header = f'Player {b_act.state["active_player"]}\'s turn'
        self.reload_screen()

        play_mode = 2

    def update(self):
        global _selected_pos, _selected, play_mode

        while True:
            print(play_mode)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.setup()

                if play_mode == 1:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if _selected:
                                new_pos = self.find_clicked_board_pos(event.pos)
                                if b_act.check_pos_empty(new_pos):
                                    self.move_obj(_selected_pos, new_pos)

                            else:
                                self.select_obj(event.pos)

                        elif event.button == 3 and _selected:
                            self.unselect_obj()

                if play_mode == 2:
                    if b_act.state["active_player"] == ai.ai_player:
                        b_act.ai_play_mode = True
                        ai.play()
                        b_act.ai_play_mode = False
                        self.update_header()

                    elif b_act.state["active_player"] == ai.ai_player % 2 + 1:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                if _selected:
                                    new_pos = self.find_clicked_board_pos(event.pos)
                                    if b_act.check_pos_empty(new_pos):
                                        self.move_obj(_selected_pos, new_pos)

                                else:
                                    self.select_obj(event.pos)

                            elif event.button == 3 and _selected:
                                self.unselect_obj()


                if event.type == pygame.MOUSEBUTTONDOWN and self.home_btn.is_clicked(event.pos):
                    sm.change_screen(sm.menuScreen)
                    pygame.quit()
            pygame.display.flip()