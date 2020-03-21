import pygame
import src.NN.MultilayerPerceptron as MLP
import src.exp_pygame.Neuron as Neuron
import src.exp_pygame.Connector as Connector
import src.exp_pygame.Button as Button
import src.exp_pygame.InputTerminal as Terminal


class Visualizer(MLP.Multilayerperceptron):
    def __init__(self, n, eta, layers, height, width):
        MLP.Multilayerperceptron.__init__(self, n, eta, layers)
        pygame.init()
        self.total_error = [0]
        self.alpha = 0.01
        self.a =  0
        self.b = 0
        self.s = 20
        self.off = 0
        self.ef = "MAE"
        self.train_dict = {1:[(0,1) ,(1, 0), (1,1)], 0:[(0,0)]}
        self.eta = eta
        self.height = height
        self.width = width
        self.win = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE, pygame.RESIZABLE or pygame.NOFRAME)
        self.viz_neurons = []
        self.connections = []
        self.update_nn()
        self.update_loop()

    def update_loop(self):
        window = True
        started = False
        key_index = 0
        value_index = 0
        while window:
            if key_index >= len(list(self.train_dict.keys())):
                key_index = 0

            key = list(self.train_dict.keys())[key_index]
            val = self.train_dict[key][value_index]

            for event in pygame.event.get():
                mx, my = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    window = False
                    pygame.display.quit()
                    exit(0)
                if event.type == pygame.VIDEORESIZE:
                    self.width = event.w
                    self.height = event.h
                    self.update_nn()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mx > self.button.get_x() and mx < self.button.get_colliding_x() and my > self.button.get_y() and my < self.button.get_colliding_y():
                        started = True
                        self.train(val, key)
                        self.update_nn()
            if started:

                    self.train(val, key)



            if self.error_function(self.total_error) <= self.alpha:
                if value_index < len(self.train_dict[key_index]):
                    value_index += 1
                else:
                    value_index = 0

                if key_index < len(list(self.train_dict.keys())):
                    if value_index > len(self.train_dict[key_index]) - 1:
                        key_index += 1
                        value_index = 0
                    else:
                        pass
                else:
                    key_index = 0


            self.update_nn()
            self.total_error = [0]


    def create(self):
        self.get_size()
        self.create_nn()
        self.create_UI()

    def create_UI(self):
        self.button = Button.Button((10, 25), "Start", (200,20), (255,0,0))
        self.button.draw(self.win)

        font = pygame.font.SysFont("Arial", 15)
        text = font.render(str(self.error_function(self.total_error)), True, (255, 255, 255))
        self.win.blit(text, (100, 100))

    def get_size(self):
        l,m = self.get_layer_max()
        off = (self.width / (1.06 * (len(list(self.neurons.keys())) - 1)))
        off_2 = (self.height / (m * 0.06 + (l -1)))
        self.b = ((l * self.s) + ((l - 2) * off)) / 2
        self.a = ((len(list(self.neurons.keys())) * self.s) + ((len(list(self.neurons.keys())) - 1) * off)) / 2

        print(self.a, self.b)

        if off > off_2:
            self.off = off_2
            self.s = int(self.off * 0.06)
        else:
            self.off = off
            self.s = int(self.off * 0.06)

    def get_layer_max(self):
        ln = 0
        for key in list(self.neurons.keys()):
            l = len(self.neurons[key])
            if l > ln:
                ln = l

        return ln, key

    def create_nn(self):

        if len(self.viz_neurons) == 0 and len(self.connections) == 0:
            for key in list(self.neurons.keys()):
                for neuron in self.neurons[key]:
                    index = self.neurons[key].index(neuron)
                    pos = (len(self.neurons[key]) / 2) * self.off
                    x = int((key * self.off) + (self.width / 2) - self.a)
                    y = int((pos - index * self.off) + (self.height  / 2) - self.b / 2)

                    c = (255, 0, 0)
                    if neuron.bias:
                        c = (155, 0, 255)

                    if key == list(self.neurons.keys())[-1] or key == list(self.neurons.keys())[0]:
                        self.viz_neurons.append(Terminal.InputTerminal(x,y, str(neuron.input),c, self.s, self.s))
                    else:
                        self.viz_neurons.append(Neuron.Neuron(x, y, str(neuron.output), c, self.s))

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
        self.win = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE or pygame.NOFRAME)
        self.viz_neurons = []
        Neuron.Neuron.id = 0
        self.connections = []
        self.create()
        self.draw()
        pygame.display.update()

    def pass_values(self, key, value):
        output_total = []
        expected_output = []
        for n in range(len(self.neurons[0])):
            neuron = self.neurons[0][n]
            neuron.clear_input()
            neuron.set_input(value[n])
            for connection in neuron.get_output_cnts():
                connection.set_input_value(value[n])

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

        return output

    @staticmethod
    def calculate_total_error(output, expected_output):
        return output - expected_output

    def back_propagation(self, total_error):
        key_list = list(self.neurons.keys())
        key_list.reverse()
        for key in key_list:
            for neuron in self.neurons[key]:
                if key == key_list[0]:
                    neuron.e = neuron.activation_function_derivatives(neuron.scalar_product()) * total_error

                for input in neuron.get_input_cnts():
                    neuron2 = input.get_input_neuron()
                    neuron2.e += neuron.e * input.get_weight() * neuron2.activation_function_derivatives(
                        neuron2.scalar_product())

    def update_weights(self):
        for key in list(self.neurons.keys()):
            for neuron in self.neurons[key]:
                for cnt in neuron.get_input_cnts():
                    inp = cnt.get_input_neuron().generate_output()
                    cnt.update_weight(-neuron.e * self.eta * inp)

    def error_function(self, total_error):
        try:
            total_error = total_error[1:]
            if self.ef == "MSE":
                return self.MSE(total_error)
            if self.ef == "MAE":
                return self.MAE(total_error)
            if self.ef == "RMSE":
                return self.RMSE(total_error)
        except ZeroDivisionError:
            return 0

    def clear_e(self):
        for key in list(self.neurons.keys()):
            for neuron in self.neurons[key]:
                neuron.e = 0

    def MSE(self, total_error):
        return (1/len(total_error) * (sum(total_error) ** 2))

    def RMSE(self, total_error):
        return self.MSE(total_error) ** 0.5

    def MAE(self, total_error):
        return (1/len(total_error) * (sum([abs(e) for e in total_error])))

    def train(self, inp, expected):
        self.output = self.pass_values(expected, inp)
        total_error = self.calculate_total_error(self.output, expected)
        self.total_error.append(total_error)
        self.back_propagation(total_error)
        self.update_weights()
        self.clear_e()


v = Visualizer(1, 0.01,[2,3,1], 600, 800)