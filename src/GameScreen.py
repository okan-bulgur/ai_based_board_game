from src.Screen import Screen
from src.Button import Button
from src import ScreenManager as sm

from abc import ABC
import sys
import pygame

SCREEN_COLOR = (255, 255, 255)
CAPTION = 'AI Based Board Game'

HEADER_POS_Y = 75
HEADER_FONT_SIZE = 70
HEADER_FONT_NAME = 'arialblack'
HEADER_COLOR = (0, 0, 0)

HOME_BTN_SIZE = 50
HOME_BTN_GAP = 70


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
        self.home_btn = Button(self.sw-HOME_BTN_GAP, HOME_BTN_GAP - HOME_BTN_SIZE, HOME_BTN_SIZE, HOME_BTN_SIZE,
                               btn_color=SCREEN_COLOR, icon=home_img)
        self.home_btn.draw(self.screen)

    def setup(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.sw, self.sh))
        self.screen.fill(SCREEN_COLOR)
        pygame.display.set_caption(CAPTION)

        self.setup_header(HEADER_FONT_NAME, HEADER_FONT_SIZE, self.header_txt, HEADER_COLOR, HEADER_POS_Y)
        self.setup_home_btn()

    def update(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.home_btn.is_clicked(event.pos):
                        sm.change_screen(sm.menuScreen)
                        pygame.quit()

            pygame.display.update()

