import pygame
import src.exp_pygame.Neuron as Neuron

class InputTerminal(Neuron.Neuron):
    def __init__(self, x ,y , text, color, size_x, size_y):
        Neuron.Neuron.__init__(self, x, y, text, color, 0)
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y

    def draw(self, win):
        pygame.draw.rect(win, self.c, (self.x, self.y, self.size_x, self.size_y))
        font = pygame.font.SysFont("Arial", 15)
        text = font.render(self.text, True, (255, 255, 255))
        win.blit(text, (self.x, self.y))


