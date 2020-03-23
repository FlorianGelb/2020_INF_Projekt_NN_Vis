import pygame

class Neuron():

    id = 0

    def __init__(self, x, y, text, c, s, font):
        self.n_id = Neuron.id
        Neuron.id += 1
        self.font = font
        self.x = x
        self.y = y
        self.text = text
        self.c = c
        self.s = s

    def draw(self, win):
        pygame.draw.circle(win, self.c, (self.x, self.y), self.s)
        text = self.font.render(self.text, True, (255, 255, 255))
        win.blit(text, (self.x, self.y))
    def set_x(self, x):
        self.x = x

    def get_x(self):
        return self.x

    def set_y(self, y):
        self.y = y

    def get_y(self):
        return self.y

    def get_id(self):
        return self.n_id

