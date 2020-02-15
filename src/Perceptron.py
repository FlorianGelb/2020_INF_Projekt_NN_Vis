import src.Neuron as Neuron
import src.Connector as Connector

class Perceptron:
    def __init__(self, n_inputs, eta):
        self.neuron = Neuron.Neuron(True)
        self.cnt_input = []
        self.train_data = {}
        self.n_inputs = n_inputs
        self.eta = eta * 10 ** -4
        self.neuron.set_activation_function("SINUS")
       # self.neuron.set_treshold(0.1)

        for n in range(n_inputs):
            self.cnt_input.append(Connector.Connector(None, self.neuron))

    def set_train_data(self, learn_input) :
        if len(learn_input[0][0]) != self.n_inputs:
            raise("Number of Inputs must match number of input cells")
        self.train_data = learn_input

    def get_train_data(self):
        return self.train_data

    def get_eta(self):
        return self.eta
    def set_eta(self, eta):
        self.eta = eta

    def train(self, error_level):
        inp = []
        error_dict = {}
        while True:
          #  print(error_dict)
            l = sum([len(x) for x in error_dict.values()])
            l_acceptable = sum([len(x) for x in error_dict.values() if x[0] <= error_level])
            if l_acceptable == l and l != 0:
                break
            for i in range(len(self.train_data.keys())):
                key = list(self.train_data.keys())[i]
                self.neuron.set_excepted_output(key)
                for data in self.train_data[key]:
                    for n in range(self.n_inputs):
                        self.cnt_input[n].set_input_value(data[n])
                        inp.append(self.cnt_input[n].calc_output())
                    self.neuron.clear_input()
                    self.neuron.set_input(inp)
                    error = (key - self.neuron.generate_output())
                    #print(error)
                    error_dict[data] = [error]
                    for i in range(len(inp)):
                       # print(inp[i])
                        d_w = (self.eta * error * inp[i])
                        self.cnt_input[i].update_weight(d_w)
                    inp = []
                    print(str(data) + "  " + str(self.neuron.generate_output()))





        '''for i in range(len(self.train_data.keys())):
            key = list(self.train_data.keys())[i]
            self.neuron.set_excepted_output(key)
            for data in self.train_data[key]:
                for n in range(self.n_inputs):
                    self.cnt_input[n].set_input_value(data[n])
                    inp = self.cnt_input[n].calc_output()
                    self.neuron.clear_input()
                    self.neuron.set_input(inp)
                    # print(error)
                    # print(str(n) + " " + str(self.cnt_input[n].weight) + " " + str(d_w))
'''



p = Perceptron(2, 1)
p.set_train_data({1:[(0,1),(1,0),(1,1)], 0:[(0, 0)]})
p.train(0.01)