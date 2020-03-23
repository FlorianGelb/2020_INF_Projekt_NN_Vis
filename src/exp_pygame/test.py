import pygame
import src.NN.MultilayerPerceptron as MLP
import src.exp_pygame.Neuron as Neuron
import src.exp_pygame.Connector as Connector
import src.exp_pygame.Button as Button
import src.exp_pygame.InputTerminal as Terminal
import src.exp_pygame.CheckBox as Checkbox
import random
import src.exp_pygame.Label as Label


class Visualizer(MLP.Multilayerperceptron):
    def __init__(self, n, eta, layers, width, height):
        MLP.Multilayerperceptron.__init__(self, n, eta, layers)
        pygame.init()
        self.total_error = []
        self.alpha = 0.01
        self.a =  0
        self.b = 0
        self.s = 20
        self.height = height
        self.width = width
        self.off = 0
        self.output_list = []
        self.finished = True
        self.training = True
        self.digit = 4
        self.ef = "MAE"
        self.train_dict = {1:[(0,1) ,(1, 0), (1,1)], 0:[(0,0)]}
        self.eta = eta
        self.win = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.surface = pygame.Surface((self.width, self.height))
        self.viz_neurons = []
        self.connections = []
        self.checkboxes = []
        self.labels = []
        self.create_UI()
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

            if self.training:


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
                        self.finished = False
                        self.train(val, key)
                        self.update_nn()

                    for checkbox in self.checkboxes:
                        if mx > checkbox.get_x() and mx < checkbox.get_colliding_x() and my > checkbox.get_y() and my < checkbox.get_colliding_y():
                            if not started and checkbox.ident == "TRA":
                                if checkbox.get_checked():
                                    checkbox.c = (0, 150, 0)
                                    checkbox.text = "V"
                                    self.training = not self.training
                                    key_index = 0
                                    value_index = 0
                                else:
                                    checkbox.c = (255, 0, 0)
                                    checkbox.text = "T"

                            if not started:
                                if checkbox.get_checked():
                                    if checkbox.group == 1:
                                        checkbox.c = (0, 150, 0)
                                        self.deactivate_check(checkbox.group, checkbox.ident)
                                        if checkbox.ident == "SIN":
                                            self.activation = "SINUS"
                                        if checkbox.ident == "SIG":
                                            self.activation = "SIG"
                                        if checkbox.ident == "LIN":
                                            self.activation = "LINEAR"
                                        if checkbox.ident == "REL":
                                            self.activation = "RELU"
                                        if checkbox.ident == "STP":
                                            self.activation = "STEP"
                                        if checkbox.ident == "TAN":
                                            self.activation = "TAN"

                                    if checkbox.group == 2:
                                        checkbox.c = (0, 150, 0)
                                        self.deactivate_check(checkbox.group, checkbox.ident)
                                        if checkbox.ident == "MSE":
                                            self.ef = "MSE"
                                        if checkbox.ident == "RMSE":
                                            self.ef = "RMSE"
                                        if checkbox.ident == "MAE":
                                            self.ef = "MAE"

                                    if checkbox.group == 3:
                                        checkbox.c = (0, 150, 0)
                                        key_index = 0
                                        value_index = 0
                                        self.deactivate_check(checkbox.group, checkbox.ident)
                                        if checkbox.ident == "OR":
                                            self.train_dict = {1:[(0,1) ,(1, 0), (1,1)], 0:[(0,0)]}

                                        if checkbox.ident == "AND":
                                            self.train_dict = {1: [(1, 1)], 0: [(0, 0), (0, 1), (1, 0)]}

                                        if checkbox.ident == "XOR":
                                            self.train_dict = {1: [(0, 1), (1, 0)], 0: [(0, 0), (1, 1)]}

                                else:
                                    checkbox.c = (255, 0, 0)


                            checkbox.set_checked(not checkbox.get_checked())


            if started:
                self.train(val, key)

                ##if self.error_function(self.total_error) <= self.alpha:
                if not self.training:
                    if self.error_function([self.total_error[-1]]) <= self.alpha:
                        key = random.choice(list(self.train_dict.keys()))
                        val = random.choice(self.train_dict[key])
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

                if key == list(self.train_dict.keys())[-1] and val == self.train_dict[list(self.train_dict.keys())[-1]][-1]:
                    if self.error_function(self.total_error) < self.alpha:
                        started = False
                        self.finished = True

                    self.total_error = []

            self.update_nn()

    def deactivate_check(self, g, i):
        for c in self.checkboxes:
            if c.group == g and c.ident != i:
                c.set_checked(False)
                c.c = (255, 0, 0)


    def create(self):
        self.get_size()
        self.create_nn()
        self.update_UI()


    def generate_list(self):
        l = []
        if self.finished:
            for key in list(self.train_dict.keys()):
                for val in self.train_dict[key]:
                    l.append(round(self.pass_values(key, val), 3))

            return l
        return self.output_list

    def update_UI(self):
        try:
            text = self.ef + " " + str(round(self.error_function(self.total_error), 4))
        except Exception:
            text = "0"

        font = pygame.font.SysFont("Arial", 15)
        text = font.render(text, True, (255, 255, 255))
        self.surface.blit(text, (10, 50))

        self.output_list = self.generate_list()

        font = pygame.font.SysFont("Arial", 15)
        text = font.render("Ausgaben: "+str(self.output_list), True, (255, 255, 255))
        self.surface.blit(text, (100, 50))



    def create_UI(self):

#        font = pygame.font.SysFont("Arial", 15)
#        text = font.render()
 #       self.surface.blit(text, (10, 100))
        self.labels.append(Label.Label("Aktivierungsfunktion:", True, (255, 255, 255), 15, 10, 100))
        self.labels.append(Label.Label("SIN", True, (255, 255, 255), 15, 10, 125))
        self.labels.append(Label.Label("SIG", True, (255, 255, 255), 15, 10, 150))
        self.labels.append(Label.Label("LIN", True, (255, 255, 255), 15, 10, 175))
        self.labels.append(Label.Label("TAN", True, (255, 255, 255), 15, 10, 200))
        self.labels.append(Label.Label("REL", True, (255, 255, 255), 15, 10, 225))
        self.labels.append(Label.Label("STP", True, (255, 255, 255), 15, 10, 250))

        self.labels.append(Label.Label("Fehlerfunktion", True, (255, 255, 255), 15, 10, 300))
        self.labels.append(Label.Label("MAE", True, (255, 255, 255), 15, 10, 325))
        self.labels.append(Label.Label("MSE", True, (255, 255, 255), 15, 10, 350))
        self.labels.append(Label.Label("RMSE", True, (255, 255, 255), 15, 10, 375))

        self.labels.append(Label.Label("Training", True, (255, 255, 255), 15, 10, 425))
        self.labels.append(Label.Label("OR", True, (255, 255, 255), 15, 10, 450))
        self.labels.append(Label.Label("AND", True, (255, 255, 255), 15, 10, 475))
        self.labels.append(Label.Label("XOR", True, (255, 255, 255), 15, 10, 500))

        self.button = Button.Button((10, 25), "Start", (self.s * 10, self.s), (255,0,0))

        checkbox = Checkbox.CheckBox((10, 75), "T", (self.s, self.s), (255,0,0), "TRA", 0)
        self.checkboxes.append(checkbox)

        self.checkboxes.append(Checkbox.CheckBox((35, 125), None, (self.s, self.s), (0,150,0), "SIN", 1))
        self.checkboxes[-1].set_checked(True)
        self.checkboxes.append(Checkbox.CheckBox((35, 150), None, (self.s, self.s), (255, 0, 0), "SIG", 1))
        self.checkboxes.append(Checkbox.CheckBox((35, 175), None, (self.s, self.s), (255, 0, 0), "LIN", 1))
        self.checkboxes.append(Checkbox.CheckBox((35, 200), None, (self.s, self.s), (255, 0, 0), "TAN", 1))
        self.checkboxes.append(Checkbox.CheckBox((35, 225), None, (self.s, self.s), (255, 0, 0), "RELU", 1))
        self.checkboxes.append(Checkbox.CheckBox((35, 250), None, (self.s, self.s), (255, 0, 0), "STEP", 1))

        self.checkboxes.append(Checkbox.CheckBox((50, 325), None, (self.s, self.s), (0, 150, 0), "MAE", 2))
        self.checkboxes[-1].set_checked(True)
        self.checkboxes.append(Checkbox.CheckBox((50, 350), None, (self.s, self.s), (255, 0, 0), "MSE", 2))
        self.checkboxes.append(Checkbox.CheckBox((50, 375), None, (self.s, self.s), (255, 0, 0), "RMSE", 2))

        self.checkboxes.append(Checkbox.CheckBox((50, 450), None, (self.s, self.s), (0, 150, 0), "OR", 3))
        self.checkboxes[-1].set_checked(True)
        self.checkboxes.append(Checkbox.CheckBox((50, 475), None, (self.s, self.s), (255, 0, 0), "AND", 3))
        self.checkboxes.append(Checkbox.CheckBox((50, 500), None, (self.s, self.s), (255, 0, 0), "XOR", 3))


        try:
            text = str(self.error_function(self.total_error))
        except Exception:
            text = "0"

        font = pygame.font.SysFont("Arial", 15)
        text = font.render(text, True, (255, 255, 255))
        self.surface.blit(text, (10, 50))

    def get_size(self):
        l,m = self.get_layer_max()
        off = (self.width / (1.06 * (len(list(self.neurons.keys())) - 1)))
        off_2 = (self.height / (m * 0.06 + (l -1)))

        if off > off_2:
            self.s = int(self.off * 0.06)
            self.off = off_2
        else:
            self.s = int(self.off * 0.06)
            self.off = off

        self.b = self.off / len(self.neurons[0])
        self.a = ((len(list(self.neurons.keys())) * self.s) + ((len(list(self.neurons.keys())) - 1) * self.off)) / 2

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
                    x = int((key * self.off) + (self.surface.get_size()[0] / 2) - self.a)
                    y = int((pos - index * self.off) + (self.surface.get_size()[1] / 2) - self.b)# - self.b / 2)

                    c = (255, 0, 0)
                    if neuron.bias:
                        c = (155, 0, 255)

                    if key == list(self.neurons.keys())[-1] or key == list(self.neurons.keys())[0]:
                        self.viz_neurons.append(Terminal.InputTerminal(x,y, str(neuron.input),c, self.s, self.s))
                    else:
                        self.viz_neurons.append(Neuron.Neuron(x, y, str(round(neuron.output, self.digit)), c, self.s))

            for key in list(self.neurons.keys()):
                for neuron in self.neurons[key]:
                    for cnt in neuron.get_input_cnts():
                        if cnt.get_input_neuron() is not None and cnt.get_output() is not None:
                            for n in self.viz_neurons:
                                if cnt.get_output().n_id == n.get_id():
                                    end = (n.get_x(), n.get_y())
                                if cnt.get_input_neuron().n_id == n.get_id():
                                    start = (n.get_x(), n.get_y())
                            self.connections.append(Connector.Connector(start, end, (255, 0, 0), str(round(cnt.get_weight(), self.digit))))


    def draw(self):
        for neuron in self.viz_neurons:
            neuron.draw(self.surface)

        for c in self.connections:
            c.draw(self.surface)

        for checkbox in self.checkboxes:
            checkbox.draw(self.surface)
            if self.s <= 10:
                checkbox.size_x = self.s * 2
                checkbox.size_y = self.s * 2
            else:
                checkbox.size_x = 20
                checkbox.size_y = 20

        for label in self.labels:
            label.draw(self.win)

        self.button.draw(self.surface)
        self.surface.convert()


    def update_nn(self):
        self.win = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.surface.convert_alpha()
        self.viz_neurons = []
        Neuron.Neuron.id = 0
        self.connections = []
        self.create()
        self.update_UI()
        self.draw()
        self.win.blit(self.surface, (0, 0))
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


v = Visualizer(1, 0.01,[2,4,1], 800, 600)