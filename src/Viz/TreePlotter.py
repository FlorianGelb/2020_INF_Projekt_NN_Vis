import src.Viz.CustomNode as CustomNode
import pyqtgraph as pg
import numpy as np

class TreePlot:

    def __init__(self):
        self.window = None
        self.viewbox = None
        self.tree_plot_item = None
        self.pos = np.array([[None, None]])
        self.connections = np.array([[0, 0]], dtype=int)
        self.lines = None
        self.size = []
        self.text = []
        self.color = "black"
        pg.setConfigOptions(antialias=True)
        self.tree_plot_item = CustomNode.CustomNode()
        self.symbol = []

    def add_node(self, x, y):
        buffer = np.array([[x, y]])
        if self.pos[0][0] is None:
            self.pos.put(0, [x])
            self.pos.put(1, [y])
        else:
            self.pos = np.concatenate((self.pos, buffer))

    def set_symbol(self, s):
        self.symbol.append(s)

    def update_graph(self):
        self.tree_plot_item.setData(pos=self.pos, adj=self.connections, pen=self.lines, size=self.size, symbol=self.symbol, \
                                    pxMode=False, text=self.text)

    def set_connection(self, node_index_1, node_index_2, r, g, b, a, w):

        if self.connections.size == 2 and self.connections[0][0] == 0 and self.connections[0][1] == 0:
            self.connections.put(0, [node_index_1])
            self.connections.put(1, [node_index_2])
        else:
            buffer = np.array([[node_index_1, node_index_2]])
            self.connections = np.concatenate((self.connections, buffer))
        self.set_lines(r, g, b, a, w)

    def set_node_size(self, s):
        self.size.append(s)

    def set_text(self, t):
        self.text.append(t)

    def set_color(self, c):
        self.tree_plot_item.set_color(c)

    def get_pos(self):
        return self.pos

    def set_lines(self, r, g, b, a, w):
        if self.lines is None:
            self.lines = np.array([(r, g, b, a, w)], \
                                  dtype=[('red', np.ubyte), ('green',np.ubyte), \
                                         ('blue', np.ubyte), ('alpha',np.ubyte), ('width', float)])

        else:
            buffer = np.array([(r, g, b, a, w)], dtype=[('red',np.ubyte),('green',np.ubyte),\
                                                  ('blue',np.ubyte),('alpha',np.ubyte),('width',float)])
            self.lines = np.concatenate((self.lines, buffer))