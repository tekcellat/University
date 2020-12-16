__author__ = 'monomah'


from ui_mainwindow import Ui_Form
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
import sys
import modeller


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self._ui = Ui_Form()
        self._ui.setupUi(self)

    @pyqtSlot(name='on_pushButton_clicked')
    def _parse_parameters(self):
        try:
            ui = self._ui
            uniform_a = float(ui.lineEdit_generator_a.text())
            uniform_b = float(ui.lineEdit_generator_b.text())
            expo_l = float(ui.lineEdit_servicemachine_lambda.text())
            req_count = int(ui.lineEdit_request_count.text())
            reenter = float(ui.lineEdit_reenter_probability.text())
            method = ui.comboBox_method.currentIndex()

            model = modeller.Modeller(uniform_a, uniform_b, expo_l, reenter)
            if method == 0:
                self._show_results(model.event_based_modelling(req_count))
            else:
                delta_t = float(ui.lineEdit_deltat.text())
                self._show_results(model.time_based_modelling(req_count, delta_t))
        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Ошибка в данных!')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', e)

    def _show_results(self, results):
        ui = self._ui
        ui.lineEdit_res_request_count.setText(str(results[0]))
        ui.lineEdit_res_reentered_count.setText(str(results[1]))
        ui.lineEdit_res_max_queue_size.setText(str(results[2]))
        ui.lineEdit_res_time.setText('{:.2f}'.format(results[3]))

    @pyqtSlot(int)
    def on_comboBox_method_currentIndexChanged(self, index):
        if index == 1:
            # Δt
            visibility = True
        else:
            visibility = False
            # events
        self._ui.lineEdit_deltat.setEnabled(visibility)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())
