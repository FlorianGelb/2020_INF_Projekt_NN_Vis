import src.NN.Neuron as Neuron
import src.NN.Connector as Connector

class Multilayerperceptron:
    def __init__(self, n_inputs, eta, shape):
        self.neurons = {}
        self.n_inputs = n_inputs
        self.shape = shape
        self.shape.insert(0, n_inputs * shape[0])
        self.shape.insert(-1, shape[-1])

        for n in range(len(shape))[1:-2]:
            self.shape[n] += 1


        for i in range(len(shape)):
            for j in range(shape[i]):
                n = Neuron.Neuron(i +1 == len(shape),i == 0,eta)
                n.set_treshold(-100)
                n.set_activation_function("LINEAR")
                n.set_step(False)

                if j == shape[i] -1 and shape[i] > 1:
                    n.output = 1
                    n.bias = True

                if i not in list(self.neurons.keys()):
                    self.neurons[i] = [n]
                else:
                    self.neurons[i].append(n)

        key_list = list(self.neurons.keys())
        for key_prime in key_list:
            if key_list[-1] != key_prime:
                key_secondary = key_prime + 1

            elif len(key_list) == 1:
                for i in range(len(self.neurons[key_prime])):
                    neuron1 = self.neurons[key_prime][i]
                    if len(neuron1.get_input_cnts()) < n_inputs and i != len(self.neurons[key_prime]) - 1:
                        for h in range(n_inputs):
                            neuron1.set_input_cnts(Connector.Connector(None, neuron1))
                    c = Connector.Connector(neuron1, None)
                    neuron1.add_output(c)
                    break
                break

            else:
                pass

            for i in range(len(self.neurons[key_prime])):
                for j in range(len(self.neurons[key_secondary])):
                    neuron1 = self.neurons[key_prime][i]
                    neuron2 = self.neurons[key_secondary][j]

                    if len(self.neurons[key_secondary]) > 1 and j == len(self.neurons[key_secondary]) -1:
                        break

                    if key_prime == 0:
                        break

                    if key_prime == 1 and i != len(self.neurons[key_prime]) - 1:
                        if len(neuron1.get_input_cnts()) < n_inputs:
                            for h in range(n_inputs * i, (n_inputs * i + n_inputs)):
                                connector = Connector.Connector(self.neurons[0][h], neuron1)
                                neuron1.set_input_cnts(connector)
                                self.neurons[0][h].add_output(connector)

                    elif key_prime == key_list[-2]:
                        c = Connector.Connector(neuron1, self.neurons[key_list[-1]][i])
                        neuron1.add_output(c)
                        self.neurons[key_list[-1]][i].set_input_cnts(c)

                        break

                    elif key_prime == key_list[-1]:
                        break

                    c = Connector.Connector(neuron1, neuron2)
                    neuron1.add_output(c)
                    neuron2.set_input_cnts(c)








