from src.Viz.TreePlotter import TreePlot as TP
import pyqtgraph as pg
from src.NN import MultilayerPerceptron as mlp
import time

class PlottingWidget(mlp.Multilayerperceptron):

    def __init__(self, n, eta, layers, UI):
        mlp.Multilayerperceptron.__init__(self, n, eta, layers)
        pg.setConfigOptions(antialias=True)
        self.T = TP()
        self.tree_plot_item = self.T.tree_plot_item
        self.UI = UI
        self.train({1:[(1,1)]}, 1)
        self.train({1:[(1,0)]}, 1)
        self.train({1:[(0,1)]}, 1)
        self.train({0:[(0,0)]}, 1)
        self.test()

        #self.UI.pushButton.clicked.connect(lambda:  self.train({1: [(1, 1), (1,0), (0,1)],0:[(0,0)]}, 0.1))


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
                    neuron.clear_input()
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
        for (o, e) in zip(output, total_error):
            for key in key_list:
                for neuron in self.neurons[key]:
                    if key == key_list[0]:
                        neuron.e = neuron.activation_function_derivatives(neuron.scalar_product()) * e
                       # self.update()

                    for input in neuron.get_input_cnts():
                        neuron2 = input.get_input_neuron()
                        neuron2.e += neuron.e * input.get_weight() * neuron2.activation_function_derivatives(
                            neuron2.scalar_product())
                        #self.update()

    def train(self, train_dict, alpha):
        output, expceted_output = self.pass_values(train_dict)
        total_error = self.calculate_total_error(output, expceted_output)
        self.back_propagation(total_error, output)
        quadratic_error = 0.5 * (sum(total_error) ** 2)
        #self.update()

    def test(self):
        self.t = 0
        while True:
            self.t += 1
            self.update()

    def update(self):
        self.UI.viewbox.removeItem(self.tree_plot_item)

        self.T = TP()
        self.tree_plot_item = self.T.tree_plot_item

        y_off = 10
        x_off = 5
        for key in list(self.neurons.keys()):
            for neuron in self.neurons[key]:
                index = self.neurons[key].index(neuron)
                pos = (len(self.neurons[key]) / 2) * x_off
                self.T.add_node(key * y_off,  pos - (index * x_off))

                if key == 0 or key == len(self.neurons) -1:
                    self.T.set_symbol('s')
                    self.T.set_node_size(0.5)
                    self.T.set_text(str(neuron.e))
                else:
                    self.T.set_symbol('o')
                    self.T.set_node_size(1)
                    self.T.set_text(str(self.t))

        for key in list(self.neurons.keys()):
            for neuron in self.neurons[key]:
                for cnt in neuron.get_input_cnts():
                    if cnt.get_input_neuron() is not None and cnt.get_output() is not None:
                        self.T.set_connection(cnt.get_input_neuron().n_id, cnt.get_output().n_id, 255,255,255,255, 1)
        self.T.update_graph()
        self.UI.viewbox.addItem(self.tree_plot_item)