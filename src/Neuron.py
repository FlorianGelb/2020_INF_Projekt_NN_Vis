import src.Connector

class Neuron:

    learn_rule = None
    threshold = 1
    activation_function_type = "RELU"
    id = 0

    def __init__(self, input_state, output_state, eta):

        self.id += 1
        self.n_id = self.id
        self.input_state = input_state
        self.output_state = output_state
        self.input = []
        self.output = []
        self.eta = eta
        self.output_to_neuron = []

    def add_output(self, c):
        self.output_to_neuron.append(c)

    def remove_output(self, c):
        for n in self.output_to_neuron:
            if n == c:
                self.output_to_neuron.remove(n)

    def set_learn_rule(self, s):
        self.learn_rule = s

    def get_learn_rule(self):
        return self.learn_rule

    def get_id(self):
        return self.id

    def set_input(self, input):
        self.input.append(input)

    def set_treshold(self, t):
        self.threshold = t

    def set_activation_function(self, af):
        self.activation_function_type = af

    def get_activation_function(self):
        return self.activation_function_type

    def scalar_product(self):
        sum = 0
        for input in self.input:
            sum += input #Wird im Connectorobjekt bereits mit Gewicht multipliziert
        return sum

    def activation_function(self, x):
        if self.activation_function_type == "RELU":
            return self.relu(x)
        if self.activation_function_type == "LINEAR":
            return self.linear(x)

    def relu(self, x):
        if x < 0:
            return 0
        else:
            return self.linear(x)

    @staticmethod
    def linear(x):
        return x

    def generate_output(self):
        ''' Muss erst Connector Klasse implementieren'''
        new_output = self.activation_function(self.scalar_product())
        if new_output >= self.threshold:
            self.output.append(new_output)

