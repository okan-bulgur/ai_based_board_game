from src.Screen import Screen
from src.Button import Button
from src import ScreenManager as sm

from abc import ABC
import sys
import pygame

SCREEN_COLOR = (255, 244, 234)
CAPTION = 'AI Based Board Game'

BTN_COLOR = (126, 172, 181)
BTN_FONT_SIZE = 25
BTN_FONT_NAME = 'arialblack'
BTN_TEXT_COLOR = (255, 244, 234)
BTN_WIDTH = 300
BTN_HEIGHT = 150
BTN_GAP = 100

HEADER_POS_Y = 75
HEADER_FONT_SIZE = 70
HEADER_FONT_NAME = 'arialblack'
HEADER_TXT = 'AI Based Board Game'
HEADER_COLOR = (201, 104, 104)

class MenuScreen(Screen, ABC):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MenuScreen, cls).__new__(cls)
        return cls._instance

    def __init__(self, sw=0, sh=0):
        super().__init__(sw, sh)
        self.button1 = Button
        self.button2 = Button
        self.screen = None

    def setup_btn(self):
        btn_font = pygame.font.SysFont(BTN_FONT_NAME, BTN_FONT_SIZE)
        btn_pos_y = (self.sh - (BTN_WIDTH // 2)) // 2

        btn_pos_x1 = (self.sw - (2 * BTN_WIDTH + BTN_GAP)) // 2
        btn_pos_x2 = btn_pos_x1 + BTN_WIDTH + BTN_GAP

        self.button1 = Button(btn_pos_x1, btn_pos_y, BTN_WIDTH, BTN_HEIGHT, 'HUMAN VS HUMAN',
                              BTN_TEXT_COLOR, btn_font, BTN_COLOR)
        self.button1.draw(self.screen)

        self.button2 = Button(btn_pos_x2, btn_pos_y, BTN_WIDTH, BTN_HEIGHT, 'HUMAN VS AI',
                              BTN_TEXT_COLOR, btn_font, BTN_COLOR)
        self.button2.draw(self.screen)

    def setup(self):

        self.screen = pygame.display.set_mode((self.sw, self.sh))
        self.screen.fill(SCREEN_COLOR)
        pygame.display.set_caption(CAPTION)

        self.setup_header(self.screen, HEADER_FONT_NAME, HEADER_FONT_SIZE, HEADER_TXT, HEADER_COLOR, HEADER_POS_Y)
        self.setup_btn()

    def update(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button1.is_clicked(event.pos):
                        sm.gameScreen.play_mode = 1
                        sm.change_screen(sm.gameScreen)
                        pygame.quit()
                    elif self.button2.is_clicked(event.pos):
                        sm.gameScreen.play_mode = 2
                        sm.change_screen(sm.gameScreen)
                        pygame.quit()

            pygame.display.update()