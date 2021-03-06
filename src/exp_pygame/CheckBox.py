import pygame


class CheckBox:
    def __init__(self, pos,text,size, color, ident, group):
        self.group = group
        self.ident = ident
        self.x, self.y = pos
        self.size_x, self.size_y = size
        self.text = text
        self.font = pygame.font.SysFont("Arial", 15)
        self.c = color
        self.checked = False

    def draw(self, win):
        pygame.draw.rect(win, self.c, (self.x, self.y, self.size_x, self.size_y))
        if self.text is not None:
            text = self.font.render(self.text, True, (255, 255, 255))
            win.blit(text, (self.x, self.y))

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_colliding_x(self):
        return self.x + self.size_x

    def get_colliding_y(self):
        return self.y + self.size_y

    def get_checked(self):
        return self.checked

    def set_checked(self, checked):
        self.checked = checked