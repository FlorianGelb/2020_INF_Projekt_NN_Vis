import pygame

class Label:
    def __init__(self, text, aa, c, s, x, y, font):
        self.text = text
        self.aa = aa
        self.c = c
        self.s = s
        self.x = x
        self.y = y
        self.font = font

    def draw(self, win):
        text = self.font.render(self.text, self.aa, self.c)
        win.blit(text, (self.x, self.y))