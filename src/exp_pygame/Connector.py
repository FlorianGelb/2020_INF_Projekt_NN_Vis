import pygame


class Connector:

    def __init__(self, start, end, c, text, font):
        self.start = start
        self.end = end
        self.color = c
        self.text = text
        x_start, y_start = self.start
        x_end, y_end = self.end
        self.v_x = x_end - x_start
        self.v_y = y_end - y_start
        self.x = int(x_start + 0.2 * self.v_x)
        self.y = int(y_start + 0.2 * self.v_y)
        self.font = font

    def draw(self, win):
        pygame.draw.aaline(win, self.color, self.start, self.end)
        text = self.font.render(self.text, True, (255, 255, 255))
        win.blit(text, (self.x, self.y))

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
