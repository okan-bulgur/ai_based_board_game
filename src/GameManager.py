import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame

from MenuScreen import MenuScreen
from src import ScreenManager as sm

if __name__ == '__main__':
    pygame.init()
    menuScreen = MenuScreen()
    sm.change_screen(menuScreen)