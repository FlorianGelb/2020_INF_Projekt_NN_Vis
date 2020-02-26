import src.Neuron as Neuron
import src.Connector as Connector

class Multilayerperceptron:
    def __init__(self, n_inputs, eta, shape):
        self.neurons = {}
        self.n_inputs = n_inputs

        for i in range(len(shape)):
            for j in range(shape[i]):
                n = Neuron.Neuron(shape[-1] == shape[i])
                n.set_treshold(0.4)
                n.set_activation_function("LINEAR")
                n.set_step(False)
                if i not in list(self.neurons.keys()):
                    self.neurons[i] = [n]
                else:
                    self.neurons[i].append(n)
        print(self.neurons)
        key_list = list(self.neurons.keys())
        for key_prime in key_list:
            if key_list[-1] != key_prime:
                key_secondary = key_prime + 1
            else:
                pass

            for i in range(len(self.neurons[key_prime])):
                for j in range(len(self.neurons[key_secondary])):
                    neuron1 = self.neurons[key_prime][i]
                    neuron2 = self.neurons[key_secondary][j]

                    if key_prime == 0:
                        for h in range(n_inputs):
                            neuron1.set_input_cnts(Connector.Connector(None, neuron1))

                    elif key_prime == key_list[-1]:
                        c = Connector.Connector(neuron1, neuron2)
                        neuron1.add_output(c)
                        neuron2.set_input_cnts(c)
                        break

                    c = Connector.Connector(neuron1, neuron2)
                    neuron1.add_output(c)
                    neuron2.set_input_cnts(c)

    def train(self, train_dict):
        for a in range(len(list(self.neurons.keys()))):
            for b in range(len(self.neurons[a])):
                n = self.neurons[a][b]
                sample = None
                cnts = n.get_input_cnts()
                otps = n.get_output_cnts()

                if a == 0:
                    for k in list(train_dict.values()):
                        if len(self.neurons[a]) * self.n_inputs == len(k):
                            for l in k:
                                sample = l
                                for o in range(len(l)):
                                    n.clear_input()
                                    cnts[o].set_input_value(l[o])

                                n.fetch_input()
                                #print("{}  {}".format(sample, n.generate_output()))

                                for o in otps:
                                    o.set_input_value(n.generate_output())

                        else:
                            raise Exception ("Input Dimensions must match topography")

                n.clear_input()
                n.fetch_input()
                print(n.generate_output())
                for o in otps:
                    o.set_input_value(n.generate_output())


        #print("{}  {}".format(sample, self.neurons[list(self.neurons.keys())[1]][-1].generate_output()))




m = Multilayerperceptron(2, 2, [1, 1, 1])

m.train(
    {1: [(1, 0), (0, 1)], 0: [(1, 1), (0, 0)]}
)
