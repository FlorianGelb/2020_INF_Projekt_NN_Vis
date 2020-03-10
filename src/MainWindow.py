from src.Viz.TreePlotter import TreePlot as TP
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from src.NN import MultilayerPerceptron as mlp


class PlottingWidget(mlp.Multilayerperceptron):

    def _init__(self, n, eta, layers):
        mlp.Multilayerperceptron.__init__(n, eta, layers)
        pg.setConfigOptions(antialias=True)

        self.w = pg.GraphicsWindow()
        self.w.setWindowTitle('pyqtgraph example: GraphItem')
        self.v = self.w.addViewBox()
        self.v.setAspectLocked()
        self.T = TP()
        self.v.addItem(T.tree_plot_item)


        y_off = 10
        x_off = 5


for key in m.neurons:
    pos = 0
    for neuron in m.neurons[key]:
        index = m.neurons[key].index(neuron)
        pos = (len(m.neurons[key]) / 2) * x_off
        T.add_node(key * y_off,  pos - (index * x_off))
        T.set_text(str(neuron.n_id))

for key in m.neurons:
    for neuron in m.neurons[key]:
        for cnt in neuron.get_input_cnts():
            if cnt.get_input_neuron() is not None and cnt.get_output() is not None:
                T.set_connection(cnt.get_input_neuron().n_id, cnt.get_output().n_id, 255,255,255,255, 1)
T.update_graph()
v.addItem(T.tree_plot_item)
m.train({1: [(1,1), (0,1), (1,0)], 0:[(0,0)]}, 0.25)



if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()



