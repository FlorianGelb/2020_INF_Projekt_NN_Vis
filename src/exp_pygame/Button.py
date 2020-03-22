import pygame
import src.exp_pygame.ChildObject as ChildObject
import src.exp_pygame.Label as Label


class Button(ChildObject.ChildObject):
    def __init__(self, pos,text,size, color):
        self.x, self.y = pos
        self.size_x, self.size_y = size
        self.text = text
        self.c = color
        self.rendered = [pygame.Surface(size)]
        self.rendered[0].fill((color))
        font = Label.Label("Arial", 15, self.x, self.y, self.text,  True, (255, 255, 255))
        self.rendered.append(font.get_rendered()[0])
        self.rendered[0].convert()

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_colliding_x(self):
        return self.x + self.size_x

    def get_colliding_y(self):
        return self.y + self.size_y

