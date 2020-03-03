import src.Neuron as Neuron
import src.Connector as Connector

class Multilayerperceptron:
    def __init__(self, n_inputs, eta, shape):
        self.neurons = {}
        self.n_inputs = n_inputs
        self.shape = shape

        for i in range(len(shape)):
            for j in range(shape[i]):
                n = Neuron.Neuron(i +1 == len(shape), eta)
                n.set_treshold(0)
                n.set_activation_function("LINEAR")
                n.set_step(False)
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
                    if len(neuron1.get_input_cnts()) < n_inputs:
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

                    if key_prime == 0:
                        if len(neuron1.get_input_cnts()) < n_inputs:
                            for h in range(n_inputs):
                                neuron1.set_input_cnts(Connector.Connector(None, neuron1))

                    elif key_prime == key_list[-1]:
                        c = Connector.Connector(neuron1, None)
                        neuron1.add_output(c)
                        break


                    c = Connector.Connector(neuron1, neuron2)
                    neuron1.add_output(c)
                    neuron2.set_input_cnts(c)

    def train(self, train_dict):
        sample = None
        snp = None
        for key in list(train_dict.keys()):
            l = 0
            if type(key) == int:
                l = 1
            else:
                l = len(key)
            if l != len(self.neurons[list(self.neurons.keys())[len(self.shape) - 1]]):
                raise Exception ("Output dimensions mus match topology")


        for k in list(train_dict.values()):
            for l in k:
                for a in range(len(list(self.neurons.keys()))):
                    for b in range(len(self.neurons[a])):
                        n = self.neurons[a][b]
                        cnts = n.get_input_cnts()
                        otps = n.get_output_cnts()


                        if a == 0:
                            if len(self.neurons[a]) > 1:
                                cnts = []
                                for neuron in self.neurons[a]:
                                    for c in neuron.get_input_cnts():
                                        cnts.append(c)
                            if len(self.neurons[a]) * self.n_inputs == len(l):

                                for o in range(len(l)):
                                    sample = l[o]
                                    snp = l
                                    otps = cnts[o].get_output().get_output_cnts()
                                    #print(otps)
                                    cnts[o].get_output().clear_input()
                                    cnts[o].set_input_value(l[o])
                                    #print("{}  {}  {}".format(l, cnts[o].get_input_value(), n))
                                    cnts[o].get_output().fetch_input()
                                    for ot in otps:
                                        ot.set_input_value(cnts[o].get_output().generate_output())

                            else:
                                raise Exception ("Input dimensions must match topography")

                        #else:
                        n.clear_input()
                        n.fetch_input()


                        #print("{} {} {} {}".format(a, b, n.input ,n.generate_output()))

                        for o in otps:
                            o.set_input_value(n.generate_output())

                if a == len(self.shape) - 1:
                    for key, val in train_dict.items():
                        if snp in val:
                            expected_output = key





                output_total = []
                error_innit = []

                for output_neuron in self.neurons[list(self.neurons.keys())[len(self.shape) - 1]]:
                    output = output_neuron.generate_output()
                    output_total.append(output)

                if type(expected_output) == int:
                    expected_output = [expected_output]
                for i in range(len(expected_output)):
                    error_innit.append(output_total[i] - expected_output[i])

                #print("{} {} {} {}".format(snp, output_total, expected_output, error_innit))

                for output_neuron in self.neurons[list(self.neurons.keys())[len(self.shape) - 1]]:
                    cnts = output_neuron.get_input_cnts()
                    for c in cnts:
                        neuron = c.get_input_neuron()
                        neuron.error(error_innit * c.get_weight())









                #print("{}  {}".format(snp, self.neurons[list(self.neurons.keys())[len(self.shape) - 1]][-1].
                                      #generate_output()))




m = Multilayerperceptron(2, 0.1, [1, 1, 1])

m.train(
    {1: [(1, 0), (0, 1)], 0: [(1, 1), (0, 0)]}
)
