import pygame
import src.exp_pygame.ChildObject as ChildObject
import src.exp_pygame.Label as Label

class Neuron(ChildObject.ChildObject):

    id = 0

    def __init__(self, x, y, text, c, s):
        self.n_id = Neuron.id
        Neuron.id += 1
        self.x = x
        self.y = y
        self.text = text
        self.c = c
        self.s = s
        self.rendered = [pygame.Surface((s, s))]

        circle = pygame.draw.circle(self.c, (self.x, self.y), self.s)
        self.rendered.append(circle)
        self.rendered[0].convert()
        font = Label.Label("Arial", 15, self.text, self.x, self.y, True, (255, 255, 255))
        self.rendered.append(font.get_rendered()[0])

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

