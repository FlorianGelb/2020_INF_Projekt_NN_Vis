import math

class Neuron:

    threshold = 0
    activation_function_type = "RELU"
    id = 0

    def __init__(self, o):

        self.id += 1
        self.n_id = self.id
        self.o = o
        self.input = []
        self.output = 0
        self.output_to_neuron = []
        self.expected_output = 0

    def set_excepted_output(self, o):
        if self.o:
            self.excepted_output = o
        else:
            self.excepted_output = None

    def add_output(self, c):
        self.output_to_neuron.append(c)

    def remove_output(self, c):
        for n in self.output_to_neuron:
            if n == c:
                self.output_to_neuron.remove(n)

    def calc_error(self):
        self.d_w = - self.eta * self.error() * self.output
        return self.d_w

    def error(self):
        if self.o:

            return self.activation_function_derivatives(self.scalar_product()) * (self.output - self.expected_output)
        else:
            e = 0
            for connection in self.output_to_neuron:
                neuron = connection.get_output
                e += self.activation_function_derivatives(self.scalar_product()) * neuron.error() * connection.get_weight()
            return e

    def clear_input(self):
        self.input = []
    def get_id(self):
        return self.id

    def set_input(self, input):
        self.input = input

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
        if self.activation_function_type == "SINUS":
            return self.sinus(x)
        if self.activation_function_type == "TAN":
            return self.tan(x)
        if self.activation_function_type == "LOG10":
            return self.log_10(x)

    def activation_function_derivatives(self, x):
        if self.activation_function_type == "RELU":
            return self.der_relu(x)
        if self.activation_function_type == "LINEAR":
            return self.der_linear()
        if self.activation_function_type == "SINUS":
            return self.der_sinus(x)
        if self.activation_function_type == "TAN":
            return self.der_tan(x)
        if self.activation_function_type == "LOG10":
            return self.der_log_10(x)

    def log_10(self, x):
        math.log10(x)

    def tan(self, x):
        return math.tan(x)

    def sinus(self, x):
        return math.sin(x)

    def relu(self, x):
        if x < 0:
            return 0
        else:
            return self.linear(x)

    @staticmethod
    def linear(x):
        return x

    @staticmethod
    def der_relu(x):
        if x < 0:
            return 0
        else:
            return 1
    @staticmethod
    def der_linear():
        return 1

    @staticmethod
    def der_sinus(x):
        return math.cos(x)

    def der_tan(self, x):
        return (1/(self.der_sinus(x)**2))

    def der_log_10(self, x):
        return 1/(x * math.log(10))

    def generate_output(self):
        new_output = self.activation_function(self.scalar_product())
        #print(self.input)
        if new_output >= self.threshold:
            self.output = new_output
            return self.output
        else:
            return 0
