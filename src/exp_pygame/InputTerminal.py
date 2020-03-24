import pygame
import src.exp_pygame.Neuron as Neuron


class InputTerminal(Neuron.Neuron):
    def __init__(self, x ,y , text, color, size_x, size_y, font):
        Neuron.Neuron.__init__(self, x, y, text, color, 0, font)
        self.size_x = size_x
        self.size_y = size_y
        self.font = font

    def draw(self, win):
        pygame.draw.rect(win, self.c, (self.x, self.y, self.size_x, self.size_y))
        text = self.font.render(self.text, True, (255, 255, 255))
        win.blit(text, (self.x, self.y))


