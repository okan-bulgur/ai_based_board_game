from abc import abstractmethod

import pygame

class Screen:

    def __init__(self, sw, sh):
        self.sw = 1200
        self.sh = 900

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update(self):
        pass

    def setup_header(self, screen, font_name, font_size, text, color, pos_y):
        header_font = pygame.font.SysFont(font_name, font_size)
        res = header_font.render(text, True, color)
        res_rect = res.get_rect()
        pos_x = (self.sw - res_rect.width) // 2
        screen.blit(res, (pos_x, pos_y))