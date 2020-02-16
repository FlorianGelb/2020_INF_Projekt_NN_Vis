import src.Neuron as Neuron
import src.Connector as Connector

class Multilayerperceptron:
    def __init__(self, n_inputs, eta, shape):
        self.neurons = {}
        for i in range(len(shape)):
            print(i)
            for j in range(shape[i]):
                n = Neuron.Neuron(shape[-1] == shape[i])
                n.set_treshold(0.4)
                n.set_activation_function("LOG10")
                if i not in list(self.neurons.keys()):
                    self.neurons[i] = [n]
                else:
                    self.neurons[i].append(n)
        for key in list(self.neurons.keys())
            
        #print(self.neurons)

m = Multilayerperceptron(2,2,[3,1,3])