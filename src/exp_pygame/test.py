import pygame
import src.NN.MultilayerPerceptron as MLP
import src.exp_pygame.Neuron as Neuron
import src.exp_pygame.Connector as Connector
import src.exp_pygame.Button as Button


class Visualizer(MLP.Multilayerperceptron):
    def __init__(self, n, eta, layers, height, width):
        MLP.Multilayerperceptron.__init__(self, n, eta, layers)
        pygame.init()
        self.clock = pygame.time.Clock()
        self.height = height
        self.width = width
        self.win = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.viz_neurons = []
        self.connections = []
        self.update_loop()

    def update_loop(self):
        window = True
        while window:
            for event in pygame.event.get():
                mx, my = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    window = False
                    pygame.display.quit()
                    exit(0)
                if event.type == pygame.VIDEORESIZE:
                    self.width = event.w
                    self.height = event.h
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mx > self.button.get_x() and mx < self.button.get_colliding_x() and my > self.button.get_y() and my < self.button.get_colliding_y():
                        self.train({1: [(1, 1), (1, 0), (0, 1)], 0: [(0, 0)]}, 1)

            self.update_nn()

    def create(self):
        self.create_nn()
        self.create_UI()

    def create_UI(self):
        self.button = Button.Button((10, 25), "text", (200,20), (255,0,0))
        self.button.draw(self.win)


    def create_nn(self):
        x_off = 100
        y_off = 100

        if True:# len(self.viz_neurons) == 0:# and len(self.connections) == 0:
            for key in list(self.neurons.keys()):
                for neuron in self.neurons[key]:
                    index = self.neurons[key].index(neuron)
                    pos = (len(self.neurons[key]) / 2) * x_off
                    x = int((self.width / 2) + (key * x_off))
                    y = int((self.height / 2) + (pos - index * y_off))
                    self.viz_neurons.append(Neuron.Neuron(x, y, str(neuron.input), (255, 0, 0)))

            for key in list(self.neurons.keys()):
                for neuron in self.neurons[key]:
                    for cnt in neuron.get_input_cnts():
                        if cnt.get_input_neuron() is not None and cnt.get_output() is not None:
                            for n in self.viz_neurons:
                                if cnt.get_output().n_id == n.get_id():
                                    end = (n.get_x(), n.get_y())
                                if cnt.get_input_neuron().n_id == n.get_id():
                                    start = (n.get_x(), n.get_y())
                            self.connections.append(Connector.Connector(start, end, (255, 0, 0), str(cnt.get_weight())))

    def draw(self):
        for neuron in self.viz_neurons:
            neuron.draw(self.win)

        for c in self.connections:
            c.draw(self.win)

    def update_nn(self):
        self.win = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.viz_neurons = []
        Neuron.Neuron.id = 0
        self.connections = []
        self.create()
        self.draw()

        pygame.display.update()

    def pass_values(self, train_dict):
        output_total = []
        expected_output = []

        for key in train_dict.keys():
            for value in train_dict[key]:

                '''
                Distrubutes all input values to input nodes
                '''
                for n in range(len(self.neurons[0])):
                    neuron = self.neurons[0][n]
                    neuron.clear_input()
                    neuron.set_input(value[n])
                    for connection in neuron.get_output_cnts():
                        connection.set_input_value(value[n])

                    self.update_nn()
                neuron_key_list = list(self.neurons.keys())[1:]

                for neuron_key in neuron_key_list:
                    if neuron_key == neuron_key_list[-1]:
                        for output_neuron in self.neurons[neuron_key]:
                            output_neuron.fetch_input()
                            for output in output_neuron.input:
                                output_total.append(output)
                                expected_output.append(key)
                        break

                    else:
                        for neuron in self.neurons[neuron_key]:
                            neuron.fetch_input()

                            for output_connections in neuron.get_output_cnts():
                                output_connections.set_input_value(neuron.generate_output())
                self.update_nn()

        return output_total, expected_output

    def calculate_total_error(self, output, expected_output):
        total_output_error = []
        for (o, k) in zip(output, expected_output):
            total_output_error.append(o - k)
        return total_output_error


    def back_propagation(self, total_error, output):
        key_list = list(self.neurons.keys())
        key_list.reverse()
        for (o, e) in zip(output, total_error):
            for key in key_list:
                for neuron in self.neurons[key]:
                    if key == key_list[0]:
                        neuron.e = neuron.activation_function_derivatives(neuron.scalar_product()) * e

                    for input in neuron.get_input_cnts():
                        neuron2 = input.get_input_neuron()
                        neuron2.e += neuron.e * input.get_weight() * neuron2.activation_function_derivatives(
                            neuron2.scalar_product())

    def train(self, train_dict, alpha):
        output, expceted_output = self.pass_values(train_dict)
        total_error = self.calculate_total_error(output, expceted_output)
        self.back_propagation(total_error, output)
        quadratic_error = 0.5 * (sum(total_error) ** 2)





v = Visualizer(1,1,[2,3,1], 600, 800)
