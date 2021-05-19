import main_window
from PyQt5.QtWidgets import *
from random import random, seed
from Queue import *
import numpy.random as nr
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MainWindow(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.process)
##        self.pushButton.clicked.connect(self.mass_experiment)
        self.pushButton_2.clicked.connect(self.pfe)
        self.lab1 = []

        self.fig1 = Figure()
        self.axes1 = self.fig1.add_subplot(111)
        self.graph_1 = FigureCanvas(self.fig1)

        self.verticalLayout_7.insertWidget(0, self.graph_1)

    def show_warning(self, txt=""):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Некорректные данные: " + txt)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

##    def generate_mean(self):
##        a = abs(float(self.doubleSpinBox.value()))
##        b = abs(float(self.doubleSpinBox_2.value()))
    def generate_mean(self, a, b):
        if a > b:
            a, b = b, a
        return nr.uniform(a, b)

##    def generate_Rayleigh(self):
##        sigma = float(self.doubleSpinBox_7.value())
    def generate_Rayleigh(self, sigma):
        if sigma < 0:
            sigma = abs(sigma)

        return nr.rayleigh(1 / sigma)

    def dt_principle(self, a, b, sigma):
##    def dt_principle(self, requests, sigma, a, b):
        current_time = 0
        dt = 0.001
        time_scale = 0
        wait_time = 0
        process_time_scale = 0
        queued_time = 0
        requests_amount = int(self.spinBox.value())
##        requests_amount = requests

        cur_proc_requests = 0
##        current_request_time = self.generate_mean()
##        current_process_time = self.generate_Rayleigh()
        current_request_time = self.generate_mean(a, b)
        current_process_time = self.generate_Rayleigh(sigma)
        my_queue = Queue()
        while cur_proc_requests < requests_amount:
            if time_scale >= current_request_time:
                time_scale = 0
##                current_request_time = self.generate_mean()
                current_request_time = self.generate_mean(a, b)

                my_queue.add_request(current_time)

            if my_queue.size == 0:
                wait_time += dt

            elif process_time_scale >= current_process_time:
                process_time_scale = 0
##                current_process_time = self.generate_Rayleigh()
                current_process_time = self.generate_Rayleigh(sigma)

                queued_time += my_queue.remove_request(current_time) - process_time_scale
                cur_proc_requests += 1
            else:
                process_time_scale += dt

            current_time += dt
            time_scale += dt

        req_intensity = (requests_amount + my_queue.size) / current_time
        proc_intensity = requests_amount / (current_time - wait_time)
        loading = (requests_amount + my_queue.size) * (current_time - wait_time) / \
              requests_amount / current_time

        self.doubleSpinBox_9.setValue(proc_intensity)
        self.doubleSpinBox_6.setValue(req_intensity)
        self.doubleSpinBox_5.setValue(loading)

        return loading, queued_time / requests_amount

    def pfe(self):
        lambda_1 = self.doubleSpinBox_11.value()
        lambda_2 = self.doubleSpinBox_12.value()
        mu_1 = self.doubleSpinBox_13.value()
        mu_2 = self.doubleSpinBox_14.value()
        sigma_1 = self.doubleSpinBox_15.value()
        sigma_2 = self.doubleSpinBox_16.value()

        args = []
        for i in range(8):
            args.append([])
            for j in range(8):
                args[-1].append(float(self.tableWidget_2.item(i, j).text()))

        y = []
        for i in range(8):
            a = lambda_1 if args[i][1] < 0.0 else lambda_2
            b = mu_1 if args[i][2] < 0.0 else mu_2
            sigma = sigma_1 if args[i][3] < 0.0 else sigma_2

            y.append(self.dt_principle(a, b, sigma)[1])

            print(a, b, sigma, y[-1])

            self.tableWidget.item(i, 4).setText("{:0.2f}".format(y[-1]))
            self.tableWidget_2.item(i, 8).setText("{:0.2f}".format(y[-1]))

        b = [sum([args[i][j] * y[i] / 8 * (5-1) for i in range(8)]) for j in range(8)]
        
        for i in range(8):
            self.tableWidget.item(i, 5).setText("{:0.4f}".format(sum([b[j] * \
                args[i][j] for j in range(4)])))
        
        for i in range(8):
            self.tableWidget_2.item(i, 9).setText("{:0.5f}".format(sum([b[j] * \
                args[i][j] for j in range(8)])))

        self.doubleSpinBox_20.setValue(b[0])
        self.doubleSpinBox_21.setValue(b[1])
        self.doubleSpinBox_22.setValue(b[2])
        self.doubleSpinBox_23.setValue(b[3])
        self.doubleSpinBox_24.setValue(b[4])
        self.doubleSpinBox_25.setValue(b[5])
        self.doubleSpinBox_26.setValue(b[6])
        self.doubleSpinBox_10.setValue(b[7])
        
        self.plainTextEdit.setPlainText("y = {:+0.4f} {:+0.4f} * x1 {:+0.4f} \
* x2 {:+0.4f} * x3".format(*b))
        self.plainTextEdit_2.setPlainText("y = {:+0.4f} {:+0.4f} * x1 {:+0.4f} \
* x2 {:+0.4f} * x3 {:+0.4f} * x1 * x2 {:+0.4f} * x2 * x3 {:+0.4f} * x1 * x3 \
{:+0.4f} * x1 * x2 * x3".format(*b))

    def process(self):
    ##  lab1
        self.lab1.append(self.dt_principle())
        self.lab1.sort()
##
##        with open("out.csv", "w") as f:
##            for x, y in self.lab1:
##                f.write("{};{}\n".format(x, y))
        
        self.axes1.clear()
        self.axes1.plot([x for x,y in self.lab1], \
                        [y for x,y in self.lab1])
        self.axes1.set_xlabel("Загрузка")
        self.axes1.set_ylabel("Время ожидания")
        self.graph_1.draw()

    def mass_experiment(self):
        results = [self.dt_principle(100, 0.6 + 0.4 * i, 0.0, 3.0) for i in range(500)]
##        results = [self.dt_principle(100, 6.0, 0.5 *i, 0.5 * (i+1)) for i in range(1, 51)]
        for i in range(len(results) -1, -1, -1):
            if results[i][0] > 1:
                results.pop(i)
        results.sort()

        self.axes1.clear()
        self.axes1.plot([x for x, y in results], [y for x, y in results])
        self.axes1.set_xlabel("Загрузка")
        self.axes1.set_ylabel("Время ожидания")
        self.graph_1.draw()

seed()
if __name__ == "__main__":

    import sys
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
