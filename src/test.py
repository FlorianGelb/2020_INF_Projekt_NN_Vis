import src.GUI.MainWindowGUI as MWG
from PyQt5 import QtWidgets, QtCore
import src.MainWindow as MW

class Test(MWG.Ui_MainWindow):
    tree_plot_item = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.M = MW.PlottingWidget(2, 1, [2,1,2])
        self.tree_plot_item = self.M.tree_plot_item
        self.viewbox = self.widget.addViewBox(enableMenu=False)
        self.viewbox.addItem(self.tree_plot_item)
        self.viewbox.addItem(self.tree_plot_item)
        self.M.T.update_graph()
        #self.M.train({1: [(1,1), (0,1), (1,0)], 0:[(0,0)]}, 0.19)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Test()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())