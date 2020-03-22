import pygame
import src.exp_pygame.ChildObject as ChildObject


class Label(ChildObject.ChildObject, pygame.font.Font):
    def __init__(self, font, size, x, y, text, AA, color):
        pygame.font.Font.__init__(self, pygame.font.get_default_font(), size)
        ChildObject.ChildObject.__init__(self)
        self.font = font
        self.size = size
        self.x = x
        self.y = y
        self.text = text
        self.AA = AA
        self.color = color
        self.rendered = [self.render(str(self.text), self.AA, self.color)]
