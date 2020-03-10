from src.Viz.TreePlotter import TreePlot as TP
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from src.NN import MultilayerPerceptron as mlp

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

w = pg.GraphicsWindow()
w.setWindowTitle('pyqtgraph example: GraphItem')
v = w.addViewBox()
v.setAspectLocked()


T = TP()
m = mlp.Multilayerperceptron(2, 1, [2,3,1])

print(m.neurons)
y_off = 10
x_off = 5
for key in m.neurons:
    up = []
    down = []
    l = 0
    for neuron in m.neurons[key]:
        pos = m.neurons[key].index(neuron) + 2
        if len(m.neurons[key]) > l:
         l = len(m.neurons[key])
        T.add_node(key * y_off, (l / 2) - (l * x_off))

T.set_text("a")
T.update_graph()

v.addItem(T.tree_plot_item)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()



