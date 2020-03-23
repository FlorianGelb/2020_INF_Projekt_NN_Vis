import pygame

class Label:
    def __init__(self, text, aa, c, s, x, y):
        self.text = text
        self.aa = aa
        self.c = c
        self.s = s
        self.x = x
        self.y = y

    def draw(self, win):
        font = pygame.font.SysFont("Arial", 15)
        text = font.render(self.text, self.aa, self.c)
        win.blit(text, (self.x, self.y))