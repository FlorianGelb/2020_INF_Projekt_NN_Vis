import pygame


class Button:
    def __init__(self, pos, text,size, color):
        self.x, self.y = pos
        self.size_x, self.size_y = size
        self.text = text
        self.c = color

    def draw(self, win, font):
        pygame.draw.rect(win, self.c, (self.x, self.y, self.size_x, self.size_y))
        text = font.render(self.text, True, (255, 255, 255))
        win.blit(text, (self.x, self.y))

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, x):
        self.x = x

    def set_size(self, size):
        self.size_x, self.size_y = size

    def set_y(self, y):
        self.y = y

    def get_colliding_x(self):
        return self.x + self.size_x

    def get_colliding_y(self):
        return self.y + self.size_y