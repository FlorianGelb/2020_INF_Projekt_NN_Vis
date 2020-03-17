from src.Viz.TreePlotter import TreePlot as TP
import pyqtgraph as pg
from src.NN import MultilayerPerceptron as mlp


class PlottingWidget(mlp.Multilayerperceptron):

    def __init__(self, n, eta, layers):
        mlp.Multilayerperceptron.__init__(self, n, eta, layers)
        pg.setConfigOptions(antialias=True)
        self.T = TP()
        self.tree_plot_item = self.T.tree_plot_item

        y_off = 10
        x_off = 5

        for key in self.neurons:
            for neuron in self.neurons[key]:
                index = self.neurons[key].index(neuron)
                pos = (len(self.neurons[key]) / 2) * x_off
                self.T.add_node(key * y_off,  pos - (index * x_off))

                if key == 0 or key == len(self.neurons) -1:
                    self.T.set_symbol('s')
                    self.T.set_node_size(0.5)
                    self.T.set_text(str(neuron.input))
                else:
                    self.T.set_symbol('o')
                    self.T.set_node_size(1)
                    self.T.set_text(str(neuron.n_id))




        for key in self.neurons:
            for neuron in self.neurons[key]:
                for cnt in neuron.get_input_cnts():
                    if cnt.get_input_neuron() is not None and cnt.get_output() is not None:
                        self.T.set_connection(cnt.get_input_neuron().n_id, cnt.get_output().n_id, 255,255,255,255, 1)








        #self.train({1: [(1,1), (0,1), (1,0)], 0:[(0,0)]}, 0.25)






