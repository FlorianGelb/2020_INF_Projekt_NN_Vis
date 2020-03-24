import random


class Connector:
    id = 0

    def __init__(self, input_from, output_to):
        self.c_id = Connector.id
        Connector.id += 1
        self.input_from = input_from
        self.output_to = output_to
        self.input_value = 0
        self.output_value = 0
        self.dbg_w_array = []
        self.dbg_dw_array = []
        self.bias = False

        if self.bias:
            self.weight = 0
        else:
            self.weight = random.random()

        self.calc_output()

    def update_weight(self, d_w):
        if not self.bias:
            self.dbg_dw_array.append(d_w)
            self.set_weight(self.weight + d_w)
        else:
            self.weight = 0

    def get_output(self):
        return self.output_to

    def get_input_neuron(self):
        return self.input_from

    def set_input_value(self, val):
        self.input_value = val

    def get_input_value(self):
        return self.input_value

    def get_output_value(self):
        return self.output_value

    def set_weight(self, w):
        self.dbg_w_array.append(w)
        self.weight = w

    def get_weight(self):
        return self.weight

    def calc_output(self):
        self.output_value = self.input_value * self.weight
        return self.output_value

    def update_bias(self, b):
        self.bias = b
        if b:
            self.weight = random.random()