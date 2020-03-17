import src.NN.Neuron as Neuron
import src.NN.Connector as Connector

class Multilayerperceptron:
    def __init__(self, n_inputs, eta, shape):
        self.neurons = {}
        self.n_inputs = n_inputs
        self.shape = shape
        self.shape.insert(0, n_inputs * shape[0])
        self.shape.insert(-1, shape[-1])


        for i in range(len(shape)):
            for j in range(shape[i]):
                n = Neuron.Neuron(i +1 == len(shape),i == 0,eta)
                n.set_treshold(-1000000)
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
                        break

                    if key_prime == 1:
                        if len(neuron1.get_input_cnts()) < n_inputs:
                            for h in range(n_inputs * i, n_inputs * i + (n_inputs)):
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

    def pass_values(self, train_dict):
        output_total = []
        expected_output = []

        for key in train_dict.keys():
            for value in train_dict[key]:
                '''
                Distrubutes all input values to input nodes
                '''
                for n in range(len(self.neurons[0])):
                    neuron = self.neurons[0][n]
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
        return output_total, expected_output

    def calculate_total_error(self, output, expected_output):
        total_output_error = []
        for (o, k) in zip(output, expected_output):
            total_output_error.append(o - k)
        return total_output_error

    def back_propagation(self, total_error, output):
        key_list = list(self.neurons.keys())
        key_list.reverse()
        for key in key_list:
            for (o, e) in zip(output, total_error):
                for neuron in self.neurons[key]:
                    if key == key_list[0]:
                        print(neuron.activation_function_derivatives(neuron.scalar_product()) * e)
                        neuron.e = neuron.activation_function_derivatives(neuron.scalar_product()) * e

                    for input in neuron.get_input_cnts():
                        neuron2 = input.get_input_neuron()
                        neuron2.e += neuron.e * input.get_weight() * neuron2.activation_function_derivatives(neuron2.scalar_product())

    def train(self, train_dict, alpha):
        output, expceted_output = self.pass_values(train_dict)
        total_error = self.calculate_total_error(output, expceted_output)
        self.back_propagation(total_error, output)
        quadratic_error = 0.5 * (sum(total_error) **2)











    '''def train(self, train_dict, alpha):
        sample = None
        snp = None
        dbg_cntr = 0

        while True:
            dbg_cntr += 1
            total_ouptut_error = None
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
                                        snp = l
                                        otps = self.neurons[a][o].get_output_cnts()
                                        self.neurons[a][o].clear_input()
                                        self.neurons[a][o].set_input(l[o])
                                        self.neurons[a][o].fetch_input()

                                        for ot in otps:
                                            ot.set_input_value(cnts[o].get_output().generate_output())

                                else:
                                    raise Exception ("Input dimensions must match topography")

                            n.clear_input()
                            n.fetch_input()

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
                        error_innit.append(output_neuron.activation_function_derivatives(output_neuron.scalar_product()) * (output_total[i] - expected_output[i]))

                    for o in range(len(self.neurons[list(self.neurons.keys())[len(self.shape) - 1]])):
                        self.neurons[list(self.neurons.keys())[len(self.shape) - 1]][o].e = error_innit[o]

                    key_list = list(self.neurons.keys())
                    key_list.reverse()

                    for o in key_list:
                        for p in self.neurons[o]:
                            cnts = p.get_input_cnts()
                            for c in cnts:
                                neuron = c.get_input_neuron()
                                if neuron != None:
                                    neuron.e += p.activation_function_derivatives(p.scalar_product()) * p.e * c.get_weight()

                            for c in p.get_input_cnts():
                                #print(c)
                                if c.get_input_neuron() is None:
                                    inp = c.get_input_value()
                                else:
                                    inp = c.get_input_neuron().generate_output()
                                c.update_weight(p.calc_error(inp))
                                p.e = 0

                    print("{} {} {} {}".format(snp, output_total, expected_output, error_innit))


                    for e in error_innit:
                        if total_ouptut_error is None:
                            total_ouptut_error = 0.5* (e **2)
                        else:
                            total_ouptut_error += 0.5* (e **2)
                   # if snp == (1, 1):
                        #print("{} {} {} {} {}".format(snp, output_total, expected_output, error_innit, total_ouptut_error))

            print(total_ouptut_error)
            if total_ouptut_error <= alpha:
                break

'''

if __name__ ==  "__main__":
    m = Multilayerperceptron(2, 0.00001 , [1])

    m.train(
        {1: [(1,1)], 0: [(0, 0), (0,1), (1,0)]}, 0.01
)
