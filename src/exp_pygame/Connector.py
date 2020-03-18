import pygame

class Connector:

    def __init__(self, start, end, c):
        self.start = start
        self.end = end
        self.color = c

    def draw(self, win):
        pygame.draw.aaline(win, self.color, self.start, self.end)

    def set_start(self, start):
        self.start = start

    def get_start(self):
        return self.start

    def set_end(self, end):
        self.end = end

    def get_end(self):
        return self.end

    def set_colro(self, c):
        self.color = c

    def get_color(self):
        return self.color