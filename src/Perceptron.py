import src.Neuron as Neuron
import src.Connector as Connector
import matplotlib.pyplot as plt

class Perceptron:
    def __init__(self, n_inputs, eta):
        self.neuron = Neuron.Neuron(True)
        self.cnt_input = []
        self.train_data = {}
        self.n_inputs = n_inputs
        self.eta = eta * 10 ** -4
        self.neuron.set_activation_function("SINUS")

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
            l = sum([len(x) for x in error_dict.values()])
            l_acceptable = sum([len(x) for x in error_dict.values() if abs(x[0]) <= error_level])
            if l_acceptable == l and l != 0:
                fig = plt.figure()
                ax1 = fig.add_subplot(211)
                ax2 = fig.add_subplot(212)
                for i in self.cnt_input:
                    ax1.plot([x for x in range(len(i.dbg_w_array))], i.dbg_w_array, label=i.c_id)
                    ax2.plot([x for x in range(len(i.dbg_dw_array))], i.dbg_dw_array, label=str(i.c_id) + " dw")
    
                ax1.legend()
                ax2.legend()
                ax1.set_xlabel("Iteration")
                ax1.set_ylabel("Gewicht")
                ax2.set_xlabel("Iteration")
                ax2.set_ylabel("Änderung Gewicht")
                plt.show()
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
                    error_dict[data] = [error]
                    for i in range(len(inp)):
                        d_w = (self.eta * error * inp[i])
                        self.cnt_input[i].update_weight(d_w)
                    inp = []
                    print(str(data) + "  " + str(self.neuron.generate_output()))

p = Perceptron(2, 1)
p.set_train_data({1:[(1,1), (1,0), (0,1)], 0:[(0, 0)]})
p.train(0.001)
