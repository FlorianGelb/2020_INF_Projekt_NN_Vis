import math


class Neuron:

    threshold = 0
    activation_function_type = "LINEAR"
    Neuron_ID = 0

    def __init__(self, o,i):
        self.n_id = Neuron.Neuron_ID
        Neuron.Neuron_ID += 1
        self.o = o
        self.i = i
        self.input = []
        self.output = 0
        self.output_to_neuron = []
        self.expected_output = 0
        self.bias = 0
        self.cnt_input = []
        self.add_step = False
        self.e = 0

    def get_output_cnts(self):
        return self.output_to_neuron

    def set_step(self, s):
        self.add_step = s

    def get_step(self):
        return self.add_step

    def set_input_cnts(self, c):
        self.cnt_input.append(c)

    def get_input_cnts(self):
        return self.cnt_input

    def set_excepted_output(self, o):
        if self.o:
            self.excepted_output = o
        else:
            self.excepted_output = None

    def set_bias(self, b):
        self.bias = b

    def get_bias(self):
        return self.bias

    def add_output(self, c):
        self.output_to_neuron.append(c)

    def remove_output(self, c):
        for n in self.output_to_neuron:
            if n == c:
                self.output_to_neuron.remove(n)

    def clear_input(self):
        self.input = []

    def get_id(self):
        return self.n_id

    def fetch_input(self):
        self.clear_input()
        for cnt in self.get_input_cnts():
            self.set_input(cnt.calc_output())

    def set_input(self, input):
        self.input.append(input)

    def set_threshold(self, t):
        self.threshold = t

    def set_activation_function(self, af):
        self.activation_function_type = af

    def get_activation_function(self):
        return self.activation_function_type

    def scalar_product(self):
        sum = 0
        for input in self.input:
            sum += input
        return sum

    def activation_function(self, x):
            if self.activation_function_type == "RELU":
                return self.relu(x)
            if self.activation_function_type == "LINEAR":
                return self.linear(x)
            if self.activation_function_type == "SINUS":
                return self.sinus(x)
            if self.activation_function_type == "SIG":
                return self.sig(x)
            if self.activation_function_type == "STEP":
                return self.step(x)

    def activation_function_derivatives(self, x):
        if self.activation_function_type == "RELU":
            return self.der_relu(x)
        if self.activation_function_type == "LINEAR":
            return self.der_linear()
        if self.activation_function_type == "SINUS":
            return self.der_sinus(x)
        if self.activation_function_type == "SIG":
            return self.der_sig(x)
        if self.activation_function_type == "STEP":
            return 1


    def step(self, x):
        if x > 0:
            return 1
        return 0

    @staticmethod
    def sig(x):
        return(1/(1 + (math.e**-x )))

    @staticmethod
    def sinus(x):
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


    @staticmethod
    def der_sig(x):
        return((math.e ** -x)/((1+math.e**-x)**2))


    def generate_output(self, dbg=False):
        new_output = self.activation_function(self.scalar_product())
        if self.bias:
            return 1
        if dbg:
            print(self.input)
        if new_output > self.threshold:
            self.output = new_output
            if self.add_step and self.output > 0:
                return 1
            elif self.add_step and self.output <= 0:
                return 0
            return self.output
        else:
            return 0

