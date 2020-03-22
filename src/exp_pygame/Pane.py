import pygame


class Pane(pygame.Surface):
    def __init__(self, win):
        pygame.Surface.__init__(self, win.get_size())
        self.win = win
        self.children = []

    def draw(self):
        self.fill((20,0,0))
        for child in self.children:
            for rendered in child.get_rendered():
                print(rendered, child)
                self.blit(rendered, child.get_pos())
        self.convert()
        self.win.blit(self, (0,0))

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        if type(child) == int:
            self.children.remove(self.children[child])
        else:
            self.children.remove(child)

    def get_children(self):
        return self.children