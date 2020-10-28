import sys
import ui_form
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QListWidget, QListWidgetItem
import markov

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = ui_form.Ui_Form()
        self.ui.setupUi(self)
        self.ui.tableWidgetMatrix.horizontalHeader().setDefaultSectionSize(30)

    @pyqtSlot()
    def on_pushButtonSolve_clicked(self):
        self.ui.listWidgetSolution.clear()
        for state in markov.getSystemTimes(self._getMatrixFromTable()):
            QListWidgetItem("{time:0.3f}".format(time = state), self.ui.listWidgetSolution)

    @pyqtSlot('int')
    def on_spinBoxStatesCount_valueChanged(self, value):
        self.ui.tableWidgetMatrix.setRowCount(value)
        self.ui.tableWidgetMatrix.setColumnCount(value)
        self.ui.tableWidgetMatrix.clearContents()

    def _getMatrixFromTable(self):
        res = []
        try:
            for i in range(self.ui.tableWidgetMatrix.rowCount()):
                row = []
                for j in range(self.ui.tableWidgetMatrix.columnCount()):
                    val = self.ui.tableWidgetMatrix.item(i, j).text() if self.ui.tableWidgetMatrix.item(i, j) else "0"
                    row.append(float(val))
                res.append(row)
        except ValueError:
            #TODO: обработать ошибку или ограничить ввод
            print("TODO")
        return res

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
