import pyqtgraph as pg


class CustomNode(pg.GraphItem):
    def __init__(self):
        pg.GraphItem.__init__(self)
        self.text = []
        self.set_color("yellow")


    def set_color(self, col):
        if col is None:
            col == "black"

    def create_text(self, txt, pos):
        if txt and pos is not None:
            for i in range(len(txt)):
                item = pg.TextItem(txt[i])
                item.setPos(pos[i][0], pos[i][1])
                item.setParentItem(self)
                self.text.append(item)

    def setData(self, **kwds):
        t = None
        c = None
        if 'adj' in kwds:
            self.adjacency = kwds.pop('adj')
            if self.adjacency.dtype.kind not in 'iu':
                raise Exception("adjacency array must have int or unsigned type.")
            self._update()
        if 'pos' in kwds:
            self.pos = kwds['pos']
            self._update()
        if 'pen' in kwds:
            self.setPen(kwds.pop('pen'))
            self._update()
        if 'text' in kwds:
            t = kwds.get("text")
        if 'symbolPen' in kwds:
            kwds['pen'] = kwds.pop('symbolPen')
        if 'symbolBrush' in kwds:
            kwds['brush'] = kwds.pop('symbolBrush')
        self.scatter.setData(**kwds)
        self.informViewBoundsChanged()
        self.create_text(t, self.pos)