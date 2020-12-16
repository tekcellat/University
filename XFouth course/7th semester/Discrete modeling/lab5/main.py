from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
import sys
import modeller


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self._ui = uic.loadUi("window.ui", self)

    @property
    def parameters(self):
        u = self._ui
        return {
            'client_m': float(u.le_client_m.text()),
            'client_d': float(u.le_client_d.text()),
            'op0_m':    float(u.le_op0_m.text()),
            'op0_d':    float(u.le_op0_d.text()),
            'op1_m':    float(u.le_op1_m.text()),
            'op1_d':    float(u.le_op1_d.text()),
            'op2_m':    float(u.le_op2_m.text()),
            'op2_d':    float(u.le_op2_d.text()),
            'comp0_m':  float(u.le_comp0_m.text()),
            'comp1_m':  float(u.le_comp1_m.text()),
            'c_count':  float(u.le_client_count.text())
        }

    def on_pushButton_model_clicked(self):
        self._ui.le_lost_clients.setText('{:.4f}'.format(modeller.event_based_modelling(**self.parameters)))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())
