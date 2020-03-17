import src.GUI.MainWindowGUI as MWG
from PyQt5 import QtWidgets, QtCore
import src.MainWindow as MW

class Test(MWG.Ui_MainWindow):
    tree_plot_item = None

    def setupUi(self, MainWindow, UI):
        super().setupUi(MainWindow)
        self.viewbox = self.widget.addViewBox(enableMenu=False)
        self.M = MW.PlottingWidget(1, 1, [2, 3, 1], UI)
        self.tree_plot_item = self.M.tree_plot_item
        self.viewbox.addItem(self.tree_plot_item)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Test()
    ui.setupUi(MainWindow, ui)
    MainWindow.show()
    sys.exit(app.exec_())