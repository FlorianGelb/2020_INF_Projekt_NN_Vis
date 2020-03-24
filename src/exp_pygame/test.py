import pygame
import src.NN.MultilayerPerceptron as MLP
import src.exp_pygame.Neuron as Neuron
import src.exp_pygame.Connector as Connector
import src.exp_pygame.Button as Button
import src.exp_pygame.InputTerminal as Terminal
import src.exp_pygame.CheckBox as Checkbox
import src.exp_pygame.Label as Label


class Visualizer(MLP.Multilayerperceptron):
    def __init__(self, n, layers, width, height):
        MLP.Multilayerperceptron.__init__(self, n, layers)
        pygame.init()
        pygame.display.set_caption("NN")
        self.n = n
        self.layers = layers
        self.total_error = []
        self.alpha = 0.1
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
        self.eta = 0.1
        self.win = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE |  pygame.DOUBLEBUF)
        self.font = pygame.font.SysFont("Arial", 15)
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
        pygame.event.set_allowed([pygame.QUIT, pygame.VIDEORESIZE, pygame.MOUSEBUTTONDOWN])
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
                    self.win = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE | pygame.DOUBLEBUF)
                    self.update_nn()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mx > self.start.get_x() and mx < self.start.get_colliding_x() and my > self.start.get_y() and my < self.start.get_colliding_y():
                        started = True
                        self.finished = False
                        self.train(val, key)
                        self.update_nn()

                    if mx > self.stop.get_x() and mx < self.stop.get_colliding_x() and my > self.stop.get_y() and my < self.stop.get_colliding_y():
                        started = False
                        self.finished = True

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
                                    checkbox.c = (0, 150, 0)
                                    key_index = 0
                                    value_index = 0
                                    self.deactivate_check(checkbox.group, checkbox.ident)

                                    if checkbox.group == 1:
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
                                        self.update_activation()

                                    if checkbox.group == 2:
                                        if checkbox.ident == "MSE":
                                            self.ef = "MSE"
                                        if checkbox.ident == "RMSE":
                                            self.ef = "RMSE"
                                        if checkbox.ident == "MAE":
                                            self.ef = "MAE"

                                    if checkbox.group == 3:
                                        if checkbox.ident == "OR":
                                            self.train_dict = {1: [(0, 1), (1, 0), (1, 1)], 0: [(0, 0)]}

                                        if checkbox.ident == "AND":
                                            self.train_dict = {1: [(1, 1)], 0: [(0, 0), (0, 1), (1, 0)]}
#
                                        if checkbox.ident == "XOR":
                                            self.train_dict = {1: [(0, 1), (1, 0)], 0: [(0, 0), (1, 1)]}

                                    if checkbox.group == 4:
                                        if checkbox.ident == "-1":
                                            self.eta = 0.1
                                        if checkbox.ident == "-2":
                                            self.eta = 0.02
                                        if checkbox.ident == "-3":
                                            self.eta = 0.001
                                        if checkbox.ident == "-4":
                                            self.eta = 0.0001
                                        if checkbox.ident == "-5":
                                            self.eta = 0.00001

                                    if checkbox.group == 5:
                                        if checkbox.ident == "-1":
                                            self.alpha = 0.1
                                        if checkbox.ident == "-2":
                                            self.alpha = 0.01
                                        if checkbox.ident == "-3":
                                            self.alpha = 0.001
                                        if checkbox.ident == "-4":
                                            self.alpha = 0.0001
                                        if checkbox.ident == "-5":
                                            self.alpha = 0.00001

                                    if checkbox.group == 6:
                                        if checkbox.ident == "-2":
                                            self.shape = [2, 2, 1]

                                        if checkbox.ident == "-3":
                                            self.shape = [2, 3, 1]

                                        if checkbox.ident == "-4":
                                            self.shape = [2, 4, 1]

                                        if checkbox.ident == "-5":
                                            self.shape = [2, 5, 1]

                                        self.update_config()
                                else:
                                    checkbox.c = (255, 0, 0)

                            checkbox.set_checked(not checkbox.get_checked())
            if started:
                self.train(val, key)

                if not self.training:

                    if self.error_function([self.total_error[-1]]) <= self.alpha:

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
                        print(self.alpha)
                        started = False
                        self.finished = True

                        for key in list(self.train_dict.keys()):
                            for val in self.train_dict[key]:
                                print(self.pass_values(key, val), key, val)

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
                    l.append((str(val) + "-->" + str(round(self.pass_values(key, val), 5))))

            return l
        return self.output_list

    def update_UI(self):

        if self.s <= 15:
            self.font = pygame.font.SysFont("Arial", self.s)
        else:
            self.font = pygame.font.SysFont("Arial", 15)

        try:
            text = self.ef + " " + str(round(self.error_function(self.total_error), 5))
        except Exception:
            text = "0"

        text = self.font.render(text, True, (255, 255, 255))
        self.surface.blit(text, (self.s * 0.66, self.s * 3.33))

        self.output_list = self.generate_list()


        text = self.font.render("Ausgaben: "+str(self.output_list[0]), True, (255, 255, 255))
        self.surface.blit(text, (self.width - 150, 0))

        text = self.font.render("Ausgaben: " + str(self.output_list[1]), True, (255, 255, 255))
        self.surface.blit(text, (self.width - 150, 25))

        text = self.font.render("Ausgaben: " + str(self.output_list[2]), True, (255, 255, 255))
        self.surface.blit(text, (self.width - 150, 50))

        text = self.font.render("Ausgaben: " + str(self.output_list[3]), True, (255, 255, 255))
        self.surface.blit(text, (self.width - 150, 75))

        if self.s <= 15:
            new_x = self.s * 0.666
            new_y = self.s * 6.666
        else:
            new_x = 10
            new_y = 100

        for label in self.labels:
            label.set_x(new_x)
            label.set_y(new_y + (self.labels.index(label)) * self.s * 1.333)

        for checkbox in self.checkboxes:
            checkbox.set_x(new_x + 4 * self.s)
            checkbox.set_y(new_y + (self.checkboxes.index(checkbox)) * self.s * 1.333)


    def create_UI(self):
        self.labels.append(Label.Label("Aktivierungsfunktion:", True, (255, 255, 255), 15, 10, 100))
        self.labels.append(Label.Label("SIN", True, (255, 255, 255), 15, 10, 125))
        self.labels.append(Label.Label("SIG", True, (255, 255, 255), 15, 10, 150))
        self.labels.append(Label.Label("LIN", True, (255, 255, 255), 15, 10, 175))
        self.labels.append(Label.Label("REL", True, (255, 255, 255), 15, 10, 200))
        self.labels.append(Label.Label("STP", True, (255, 255, 255), 15, 10, 225))
        self.labels.append(Label.Label(None, True, (255, 255, 255), 15, 10, 250))

        self.labels.append(Label.Label("Fehlerfunktion", True, (255, 255, 255), 15, 10, 275))
        self.labels.append(Label.Label("MAE", True, (255, 255, 255), 15, 10, 300))
        self.labels.append(Label.Label("MSE", True, (255, 255, 255), 15, 10, 325))
        self.labels.append(Label.Label("RMSE", True, (255, 255, 255), 15, 10, 350))
        self.labels.append(Label.Label(None, True, (255, 255, 255), 15, 10, 375))

        self.labels.append(Label.Label("Training", True, (255, 255, 255), 15, 10, 400))
        self.labels.append(Label.Label("OR", True, (255, 255, 255), 15, 10, 425))
        self.labels.append(Label.Label("AND", True, (255, 255, 255), 15, 10, 450))
        self.labels.append(Label.Label("XOR", True, (255, 255, 255), 15, 10, 475))
        self.labels.append(Label.Label(None, True, (255, 255, 255), 15, 10, 500))

        self.labels.append(Label.Label("Lernrate:", True, (255, 255, 255), 15, 10, 525))
        self.labels.append(Label.Label("1*10^-1", True, (255, 255, 255), 15, 10, 550))
        self.labels.append(Label.Label("1 * 10^-2:", True, (255, 255, 255), 15, 10, 575))
        self.labels.append(Label.Label("1 * 10*-3:", True, (255, 255, 255), 15, 10, 600))
        self.labels.append(Label.Label("1 * 10*-4:", True, (255, 255, 255), 15, 10, 625))
        self.labels.append(Label.Label("1 * 10*-5:", True, (255, 255, 255), 15, 10, 650))
        self.labels.append(Label.Label(None, True, (255, 255, 255), 15, 10, 675))

        self.labels.append(Label.Label("Fehlerrate:", True, (255, 255, 255), 15, 10, 700))
        self.labels.append(Label.Label("1*10^-1", True, (255, 255, 255), 15, 10, 725))
        self.labels.append(Label.Label("1 * 10^-2:", True, (255, 255, 255), 15, 10, 750))
        self.labels.append(Label.Label("1 * 10*-3:", True, (255, 255, 255), 15, 10, 775))
        self.labels.append(Label.Label("1 * 10*-4:", True, (255, 255, 255), 15, 10, 800))
        self.labels.append(Label.Label("1 * 10*-5:", True, (255, 255, 255), 15, 10, 825))
        self.labels.append(Label.Label(None, True, (255, 255, 255), 15, 10, 850))

        self.labels.append(Label.Label("Anzahl Neuronen in der Hidden Layer:", True, (255, 255, 255), 15, 10, 875))
        self.labels.append(Label.Label("2", True, (255, 255, 255), 15, 10, 900))
        self.labels.append(Label.Label("3", True, (255, 255, 255), 15, 10, 925))
        self.labels.append(Label.Label("4", True, (255, 255, 255), 15, 10, 950))
        self.labels.append(Label.Label("5", True, (255, 255, 255), 15, 10, 975))


        self.start = Button.Button((10, 25), "Start", (self.s * 5, self.s), (255, 0, 0))
        self.stop = Button.Button((125, 25), "Stop", (self.s * 5, self.s), (255, 0, 0))

        checkbox = Checkbox.CheckBox((10, 75), "T", (self.s, self.s), (255,0,0), "TRA", 0)
        self.checkboxes.append(checkbox)

        self.checkboxes.append(Checkbox.CheckBox((40, 125), None, (self.s, self.s), (0,150,0), "SIN", 1))
        self.checkboxes[-1].set_checked(True)
        self.checkboxes.append(Checkbox.CheckBox((40, 150), None, (self.s, self.s), (255, 0, 0), "SIG", 1))
        self.checkboxes.append(Checkbox.CheckBox((40, 175), None, (self.s, self.s), (255, 0, 0), "LIN", 1))
        self.checkboxes.append(Checkbox.CheckBox((40, 200), None, (self.s, self.s), (255, 0, 0), "REL", 1))
        self.checkboxes.append(Checkbox.CheckBox((40, 225), None, (self.s, self.s), (255, 0, 0), "STP", 1))
        self.checkboxes.append(Checkbox.CheckBox((40, 250), None, (0, 0), (255, 0, 0), None, 0))
        self.checkboxes.append(Checkbox.CheckBox((40, 275), None, (0, 0), (255, 0, 0), None, 0))

        self.checkboxes.append(Checkbox.CheckBox((50, 300), None, (self.s, self.s), (0, 150, 0), "MAE", 2))
        self.checkboxes[-1].set_checked(True)
        self.checkboxes.append(Checkbox.CheckBox((50, 325), None, (self.s, self.s), (255, 0, 0), "MSE", 2))
        self.checkboxes.append(Checkbox.CheckBox((50, 350), None, (self.s, self.s), (255, 0, 0), "RMSE", 2))
        self.checkboxes.append(Checkbox.CheckBox((40, 375), None, (0, 0), (255, 0, 0), None, 0))
        self.checkboxes.append(Checkbox.CheckBox((40, 400), None, (0, 0), (255, 0, 0), None, 0))

        self.checkboxes.append(Checkbox.CheckBox((45, 425), None, (self.s, self.s), (0, 150, 0), "OR", 3))
        self.checkboxes[-1].set_checked(True)
        self.checkboxes.append(Checkbox.CheckBox((45, 450), None, (self.s, self.s), (255, 0, 0), "AND", 3))
        self.checkboxes.append(Checkbox.CheckBox((45, 475), None, (self.s, self.s), (255, 0, 0), "XOR", 3))
        self.checkboxes.append(Checkbox.CheckBox((40, 500), None, (0, 0), (255, 0, 0), None, 0))
        self.checkboxes.append(Checkbox.CheckBox((40, 525), None, (0, 0), (255, 0, 0), None, 0))

        self.checkboxes.append(Checkbox.CheckBox((70, 550), None, (self.s, self.s), (0, 150, 0), "-1", 4))
        self.checkboxes[-1].set_checked(True)
        self.checkboxes.append(Checkbox.CheckBox((70, 575), None, (self.s, self.s), (255, 0, 0), "-2", 4))
        self.checkboxes.append(Checkbox.CheckBox((70, 600), None, (self.s, self.s), (255, 0, 0), "-3", 4))
        self.checkboxes.append(Checkbox.CheckBox((70, 625), None, (self.s, self.s), (255, 0, 0), "-4", 4))
        self.checkboxes.append(Checkbox.CheckBox((70, 650), None, (self.s, self.s), (255, 0, 0), "-5", 4))
        self.checkboxes.append(Checkbox.CheckBox((40, 675), None, (0, 0), (255, 0, 0), None, 0))
        self.checkboxes.append(Checkbox.CheckBox((40, 700), None, (0, 0), (255, 0, 0), None, 0))

        self.checkboxes.append(Checkbox.CheckBox((70, 725), None, (self.s, self.s), (0, 150, 0), "-1", 5))
        self.checkboxes[-1].set_checked(True)
        self.checkboxes.append(Checkbox.CheckBox((70, 750), None, (self.s, self.s), (255, 0, 0), "-2", 5))
        self.checkboxes.append(Checkbox.CheckBox((70, 775), None, (self.s, self.s), (255, 0, 0), "-3", 5))
        self.checkboxes.append(Checkbox.CheckBox((70, 800), None, (self.s, self.s), (255, 0, 0), "-4", 5))
        self.checkboxes.append(Checkbox.CheckBox((70, 825), None, (self.s, self.s), (255, 0, 0), "-5", 5))
        self.checkboxes.append(Checkbox.CheckBox((40, 850), None, (0, 0), (255, 0, 0), None, 0))
        self.checkboxes.append(Checkbox.CheckBox((40, 875), None, (0, 0), (255, 0, 0), None, 0))

        self.checkboxes.append(Checkbox.CheckBox((70, 900), None, (self.s, self.s), (255, 0, 0), "-2", 6))
        self.checkboxes.append(Checkbox.CheckBox((70, 925), None, (self.s, self.s), (0, 150, 0), "-3", 6))
        self.checkboxes[-1].set_checked(True)
        self.checkboxes.append(Checkbox.CheckBox((70, 950), None, (self.s, self.s), (255, 0, 0), "-4", 6))
        self.checkboxes.append(Checkbox.CheckBox((70, 975), None, (self.s, self.s), (255, 0, 0), "-5", 6))


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
                        self.viz_neurons.append(Terminal.InputTerminal(x,y, str(neuron.input),c, self.s, self.s, self.font))
                    else:
                        self.viz_neurons.append(Neuron.Neuron(x, y, str(round(neuron.output, self.digit)), c, self.s, self.font))

            for key in list(self.neurons.keys()):
                for neuron in self.neurons[key]:
                    for cnt in neuron.get_input_cnts():
                        if cnt.get_input_neuron() is not None and cnt.get_output() is not None:
                            for n in self.viz_neurons:
                                if cnt.get_output().n_id == n.get_id():
                                    end = (n.get_x(), n.get_y())
                                if cnt.get_input_neuron().n_id == n.get_id():
                                    start = (n.get_x(), n.get_y())
                            self.connections.append(Connector.Connector(start, end, (255, 0, 0), str(round(cnt.get_weight(), self.digit)), self.font))


    def draw(self):
        for neuron in self.viz_neurons:
            neuron.draw(self.surface)

        for c in self.connections:
            c.draw(self.surface)

        for checkbox in self.checkboxes:
            if self.s <= 10:
                checkbox.size_x = self.s
                checkbox.size_y = self.s
            else:
                checkbox.size_x = 10
                checkbox.size_y = 10

            if checkbox.group != 0:
                checkbox.draw(self.surface)

        for label in self.labels:
            label.draw(self.surface, self.font)

        self.start.set_size((self.s * 5, self.s))
        self.stop.set_size((self.s * 5, self.s))
        self.stop.set_x(self.start.get_colliding_x() + self.s * 0.66)
        self.stop.set_y(self.s * 1.333)
        self.start.set_x(self.s * 0.66)
        self.start.set_y(self.s * 1.333)
        self.start.draw(self.surface, self.font)
        self.stop.draw(self.surface, self.font)
        self.surface.convert()

    def update_nn(self):
        self.surface = pygame.Surface((self.width, self.height))
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


v = Visualizer(1,[2,3,1], 1920, 1080)