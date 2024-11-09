import pygame

class Button:

    def __init__(self, x, y, w, h, text=None, text_color=(0, 0, 0), font=None, btn_color=(0, 0, 0), icon=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.text = text
        self.text_color = text_color
        self.font = font
        self.btn_color = btn_color
        self.icon = icon

    def draw_txt(self, screen):
        if self.font is not None:
            res = self.font.render(self.text, True, self.text_color)
            res_rect = res.get_rect()  # get size of the text
            pos_x = ((self.w - res_rect.width) // 2) + self.x
            pos_y = ((self.h - res_rect.height) // 2) + self.y
            screen.blit(res, (pos_x, pos_y))

    def draw_icon(self, screen):
        if self.icon:
            icon_resized = pygame.transform.scale(self.icon, (self.w, self.h))
            icon_rect = icon_resized.get_rect(center=(self.rect.centerx, self.rect.centery))
            screen.blit(icon_resized, icon_rect)

    def draw(self, screen):
        pygame.draw.rect(screen, self.btn_color, self.rect)
        if self.icon is not None:
            self.draw_icon(screen)
        if self.text is not None:
            self.draw_txt(screen)

    def is_clicked(self, pos = (0, 0)):
        return self.rect.collidepoint(pos)