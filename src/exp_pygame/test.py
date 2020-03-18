import pygame
import src.NN.MultilayerPerceptron as MLP
import src.exp_pygame.Neuron as Neuron
import src.exp_pygame.Connector as Connector


class Visualizer(MLP.Multilayerperceptron):
    def __init__(self, n, eta, layers, height, width):
        MLP.Multilayerperceptron.__init__(self, n, eta, layers)
        pygame.init()
        self.height = height
        self.width = width
        self.win = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.viz_neurons = []
        self.connections = []
        self.draw()
        self.update_loop()


    def update_loop(self):
        window = True
        while window:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    window = False
                    pygame.display.quit()
                if event.type == pygame.VIDEORESIZE:
                    self.width = event.w
                    self.height = event.h
                    self.win = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                    self.draw()
            pygame.display.update()

    def draw(self):
        x_off = 100
        y_off = 100

        for key in list(self.neurons.keys()):
            for neuron in self.neurons[key]:
                index = self.neurons[key].index(neuron)
                pos = (len(self.neurons[key]) / 2) * x_off
                x = int((self.width / 2) + (key * x_off))
                y = int((self.height / 2) + (pos - index * y_off))
                self.viz_neurons.append(Neuron.Neuron(x, y, str(neuron.get_id()), (255, 0, 0)))

        for neuron in self.viz_neurons:
            neuron.draw(self.win)

        for key in list(self.neurons.keys()):
            for neuron in self.neurons[key]:
                for cnt in neuron.get_input_cnts():
                    if cnt.get_input_neuron() is not None and cnt.get_output() is not None:
                        for n in self.viz_neurons:
                            if cnt.get_output().n_id == n.get_id():
                                end = (n.get_x(), n.get_y())
                            if cnt.get_input_neuron().n_id == n.get_id():
                                start = (n.get_x(), n.get_y())
                        self.connections.append(Connector.Connector(start, end, (255,0,0)))

        for c in self.connections:
            c.draw(self.win)








v = Visualizer(1,1,[2,3,1], 600, 800)
