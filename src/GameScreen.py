from src.Screen import Screen
from src.Button import Button
from src import ScreenManager as sm
from src import BoardAction as b_act
from src.Config import BoardConfig as bc
from src.Config import GameScreenConfig as gsc
from src import AIManager as ai

from abc import ABC
import threading
import pygame
import sys
import time

class GameScreen(Screen, ABC):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GameScreen, cls).__new__(cls)
        return cls._instance

    def __init__(self, sw=0, sh=0):
        super().__init__(sw, sh)
        self.screen = None
        self.home_btn = Button

        self.selected = False
        self.selected_pos = None
        self.header = ""
        self.play_mode = 2

        self.running = True
        self.pause_event = threading.Event()
        self.pause_event.set()
        self.update_thread = threading.Thread(target=self.update)

    def setup_home_btn(self):
        home_img = pygame.image.load('res/home.png').convert_alpha()
        home_img.fill((0, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)
        self.home_btn = Button(self.sw-gsc.HOME_BTN_GAP, gsc.HOME_BTN_GAP - gsc.HOME_BTN_SIZE, gsc.HOME_BTN_SIZE, gsc.HOME_BTN_SIZE,
                               btn_color=gsc.SCREEN_COLOR, icon=home_img)
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
                self.draw_obj((row, col), b_act.state.get_value_of_board(row, col))

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

        if b_act.state.get_value_of_board(row, col) == b_act.state.get_active_player():
            b_act.state.update_board(row, col, b_act.state.get_value_of_board(row, col) * 3)
            return True

        if b_act.state.get_value_of_board(row, col) == b_act.state.get_active_player():
            return False

    def unselect_obj(self):
        b_act.unselect_obj(self.selected_pos)
        self.selected = False
        self.selected_pos = None
        self.reload_screen()

    def select_obj(self, pos):
        self.selected = self.is_selected(pos)
        self.selected_pos = self.find_clicked_board_pos(pos) if self.selected else None
        self.reload_screen()

    def update_header(self):
        cond = b_act.control_win_cond(b_act.state)

        self.header = f'Player {b_act.state.get_active_player()}\'s turn'

        if cond != -1:
            self.header = f'Player {cond} WON'
            if cond == 0:
                self.header = f'DRAW'

        self.reload_screen()
        self.selected = False
        self.selected_pos = None

    def move_obj(self, source, dest):
        b_act.move(b_act.state, b_act.state.get_active_player(), source, dest)
        self.update_header()

    def reload_screen(self):
        self.screen.fill(gsc.SCREEN_COLOR)

        self.setup_header(self.screen, gsc.HEADER_FONT_NAME, gsc.HEADER_FONT_SIZE, self.header, gsc.HEADER_COLOR, gsc.HEADER_POS_Y)
        self.setup_home_btn()

        #Counter
        counter_text = f'Number of movements: {b_act.state.get_movement_count()} / {b_act.MAX_MOVEMENTS}'
        header_font = pygame.font.SysFont(gsc.COUNTER_FONT_NAME, gsc.COUNTER_FONT_SIZE)
        res = header_font.render(counter_text, True, gsc.COUNTER_COLOR)
        self.screen.blit(res, (gsc.COUNTER_POS_X, gsc.COUNTER_POS_Y))

        self.draw_board()

    def human_action(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.selected:
                    new_pos = self.find_clicked_board_pos(event.pos)
                    if b_act.check_pos_empty(new_pos):
                        self.move_obj(self.selected_pos, new_pos)

                else:
                    self.select_obj(event.pos)

            elif event.button == 3 and self.selected:
                self.unselect_obj()


    def ai_mode_event(self, event):
        if b_act.state.get_active_player() == ai.ai_player:
            b_act.ai_play_mode = True
            ai.play()
            b_act.ai_play_mode = False
            self.update_header()

        elif b_act.state.get_active_player()  == ai.ai_player % 2 + 1:
            self.human_action(event)

    def setup(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.sw, self.sh))
        self.screen.fill(gsc.SCREEN_COLOR)
        pygame.display.set_caption(gsc.CAPTION)

        b_act.setup_state()

        self.header = f'Player {b_act.state.get_active_player()}\'s turn'

        self.reload_screen()

        if not self.pause_event.is_set():
            self.pause_event.set()

        if not self.update_thread.is_alive():
            self.update_thread.start()


    def update(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.pause_event.clear()
                    self.setup()

                if self.play_mode == 1:
                    self.human_action(event)

                if self.play_mode == 2:
                    self.ai_mode_event(event)

                if event.type == pygame.MOUSEBUTTONDOWN and self.home_btn.is_clicked(event.pos):
                    sm.change_screen(sm.menuScreen)
                    pygame.quit()

            pygame.display.flip()
            time.sleep(0.1)