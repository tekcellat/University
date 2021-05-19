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
##        self.pushButton.clicked.connect(self.process)
        self.pushButton.clicked.connect(self.ockp)
##        self.pushButton.clicked.connect(self.mass_experiment)
##        self.pushButton_2.clicked.connect(self.dfe)
        self.pushButton_2.clicked.connect(self.ockp)
        self.lab1 = []

        for i in range(32):
            for j in range(30):
                item = QTableWidgetItem()
                
                if j == 0:
                    val = 1
                elif j == 6:
                    val = -1 if self.tableWidget_7.item(i, 4).text() != self.tableWidget_7.item(i, 5).text() else 1
                elif j == 20:
                    val = -1 if self.tableWidget_7.item(i, 4).text() != self.tableWidget_7.item(i, 6).text() else 1
                elif j == 21:
                    val = -1 if self.tableWidget_7.item(i, 5).text() != self.tableWidget_7.item(i, 6).text() else 1
                elif j < 7:
                    val = -1 if (i >> (j - 1)) & 1 else 1
                elif j < 12:
                    val = -1 if self.tableWidget_7.item(i, 1).text() != self.tableWidget_7.item(i, j - 5).text() else 1
                elif j < 16:
                    val = -1 if self.tableWidget_7.item(i, 2).text() != self.tableWidget_7.item(i, j - 9).text() else 1
                elif j < 19:
                    val = -1 if self.tableWidget_7.item(i, 3).text() != self.tableWidget_7.item(i, j - 12).text() else 1
                elif j < 21:
                    val = -1 if self.tableWidget_7.item(i, 4).text() != self.tableWidget_7.item(i, j - 14).text() else 1
                else:
                    val = 0
                
                if j < 22:
                    item.setText("{:+}".format(val))
                self.tableWidget_7.setItem(i, j, item)
        
        for i in range(32, 45):
            for j in range(30):
                item = QTableWidgetItem()
                
                if j == 0:
                    val = 1
                elif i == 44:
                    val = 0
                elif i & 1 == 0 and (i - 30) // 2 == j:
                    val = -1.74
                elif (i - 30) // 2 == j:
                    val = 1.74
                else:
                    val = 0
                
                if j < 22:
                    item.setText("{:+}".format(val))
                self.tableWidget_7.setItem(i, j, item)
        
        for i in range(45):
            for j in range(6):
                val = float(self.tableWidget_7.item(i, 1 + j).text()) ** 2 - 0.84
                self.tableWidget_7.item(i, 22 + j).setText("{:+0.4f}".format(val))

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

    def dt_principle(self, a1, b1, sigma1, a2, b2, sigma2):
##        current_time = 0
##        dt = 0.001
##        time_scale = 0
##        wait_time = 0
##        process_time_scale = 0
##        queued_time = 0
##        requests_amount = int(self.spinBox.value())
##
##        cur_proc_requests = 0
##        current_request_time = self.generate_mean(a, b)
##        current_process_time = self.generate_Rayleigh(sigma)
##        my_queue = Queue()
##        while cur_proc_requests < requests_amount:
##            if time_scale >= current_request_time:
##                time_scale = 0
##                current_request_time = self.generate_mean(a, b)
##
##                my_queue.add_request(current_time)
##
##            if my_queue.size == 0:
##                wait_time += dt
##
##            elif process_time_scale >= current_process_time:
##                process_time_scale = 0
##                current_process_time = self.generate_Rayleigh(sigma)
##
##                queued_time += my_queue.remove_request(current_time) - process_time_scale
##                cur_proc_requests += 1
##            else:
##                process_time_scale += dt
##
##            current_time += dt
##            time_scale += dt
##
##        req_intensity = (requests_amount + my_queue.size) / current_time
##        proc_intensity = requests_amount / (current_time - wait_time)
##        loading = (requests_amount + my_queue.size) * (current_time - wait_time) / \
##              requests_amount / current_time
##
##        self.doubleSpinBox_9.setValue(proc_intensity)
##        self.doubleSpinBox_6.setValue(req_intensity)
##        self.doubleSpinBox_5.setValue(loading)
##
##        return loading, queued_time / requests_amount

        dt = 0.001
        time = 0.0
        requests = int(self.spinBox.value())
        
        generator_recharge = self.generate_mean(a1, b1)
        generator_recharge2 = self.generate_mean(a2, b2)
        serve_recharge = self.generate_Rayleigh(sigma1)
        serve_recharge2 = self.generate_Rayleigh(sigma2)
        serve_downtime = 0.0
        
        generated = 0
        generated2 = 0
        generated_time = 0.0
        generated_time2 = 0.0
        served = 0
        served_time = 0.0
        served_time2 = 0.0
        waited_time = 0.0
        waiting_queue = []
        
        serving_type = 0
        
        while served < requests:
            if generator_recharge <= 0.0:
                generator_recharge = self.generate_mean(a1, b1)
                generated_time += generator_recharge
                waiting_queue.append([time, False, 1])
                generated += 1
            generator_recharge -= dt
            
            if generator_recharge2 <= 0.0:
                generator_recharge2 = self.generate_mean(a2, b2)
                generated_time2 += generator_recharge2
                waiting_queue.append([time, False, 2])
                generated2 += 1
            generator_recharge2 -= dt
            
            if len(waiting_queue):
                if not waiting_queue[0][1]:
                    serving_type = waiting_queue[0][2]
                    waiting_queue[0] = [time - waiting_queue[0][0], True, serving_type]

                if serving_type == 1:
                    if serve_recharge <= 0:
                        serve_recharge = self.generate_Rayleigh(sigma1)
                        served_time += serve_recharge
                        waited_time += waiting_queue.pop(0)[0]
                        served += 1
                    serve_recharge -= dt
                else:
                    if serve_recharge2 <= 0:
                        serve_recharge2 = self.generate_Rayleigh(sigma2)
                        served_time2 += serve_recharge2
                        waited_time += waiting_queue.pop(0)[0]
                        served += 1
                    serve_recharge2 -= dt
            else:
                serve_downtime += dt
            
            # update time
            time += dt

        queued_mean = waited_time / served

        return queued_mean

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

            y.append(self.dt_principle(a, b, sigma))

            print(a, b, sigma, y[-1])

            self.tableWidget.item(i, 4).setText("{:0.2f}".format(y[-1]))
            self.tableWidget_2.item(i, 8).setText("{:0.2f}".format(y[-1]))

        b = [sum([args[i][j] * y[i] / 8 for i in range(8)]) for j in range(8)]
        
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

    def dfe(self):
        lambda_1 = self.doubleSpinBox_11.value()
        lambda_2 = self.doubleSpinBox_12.value()
        mu_1 = self.doubleSpinBox_13.value()
        mu_2 = self.doubleSpinBox_14.value()
        sigma_1 = self.doubleSpinBox_15.value()
        sigma_2 = self.doubleSpinBox_16.value()

        lambda_3 = self.doubleSpinBox_17.value()
        lambda_4 = self.doubleSpinBox_18.value()
        mu_3 = self.doubleSpinBox_19.value()
        mu_4 = self.doubleSpinBox_27.value()
        sigma_3 = self.doubleSpinBox_28.value()
        sigma_4 = self.doubleSpinBox_29.value()

## pfe

        args_1 = []
        for i in range(64):
            args_1.append([])
            for j in range(22):
                args_1[-1].append(float(self.tableWidget_6.item(i, j).text()))
##                print(i, j)

        y = []
        for i in range(64):
            a1 = lambda_1 if args_1[i][1] < 0.0 else lambda_2
            b1 = mu_1 if args_1[i][2] < 0.0 else mu_2
            sigma1 = sigma_1 if args_1[i][3] < 0.0 else sigma_2
            a2 = lambda_3 if args_1[i][4] < 0.0 else lambda_4
            b2 = mu_3 if args_1[i][5] < 0.0 else mu_4
            sigma2 = sigma_3 if args_1[i][6] < 0.0 else sigma_4

            y.append(self.dt_principle(a1, b1, sigma1, a2, b2, sigma2))

            self.tableWidget_5.item(i, 7).setText("{:0.2f}".format(y[-1]))
##            print(i)
            self.tableWidget_6.item(i, 22).setText("{:0.2f}".format(y[-1]))

        b = [sum([args_1[i][j] * y[i] / 64 for i in range(64)]) for j in range(22)]
        
        for i in range(64):
##            print(i)
            self.tableWidget_5.item(i, 8).setText("{:0.4f}".format(sum([b[j] * \
                args_1[i][j] for j in range(7)])))
        
        for i in range(64):
            self.tableWidget_6.item(i, 23).setText("{:0.5f}".format(sum([b[j] * \
                args_1[i][j] for j in range(22)])))

        self.plainTextEdit_3.setPlainText("y = {:+0.4f} * x0 {:+0.4f} * x1 {:+0.4f} \
* x2 {:+0.4f} * x3 {:+0.4f} * x4 {:+0.4f} * x5 {:+0.4f} * x6".format(*b))
        self.plainTextEdit_4.setPlainText("y = {:+0.4f} * x0 {:+0.4f} * x1 {:+0.4f} \
* x2 {:+0.4f} * x3 {:+0.4f} * x4 {:+0.4f} * x5 {:+0.4f} * x6 {:+0.4f} * x1 * x2 \
{:+0.4f} * x1 * x3 {:+0.4f} * x1 * x4 {:+0.4f} * x1 * x5 \
{:+0.4f} * x1 * x6 {:+0.4f} * x2 * x3 {:+0.4f} * x2 * x4 {:+0.4f} * x2 * x5 \
{:+0.4f} * x2 * x6 {:+0.4f} * x3 * x4 {:+0.4f} * x3 * x5 {:+0.4f} *x3 * x6 \
{:+0.4f} * x4 * x5 {:+0.4f} * x4 * x6 {:+0.4f} * x5 * x6".format(*b))

## dfe

        args_2 = []
        for i in range(32):
            args_2.append([])
            for j in range(19):
                args_2[-1].append(float(self.tableWidget_4.item(i, j).text()))
            for j in range(3):
                args_2[-1].append(0)

        y = y[:32]
        for i in range(32):
            self.tableWidget_3.item(i, 7).setText("{:0.2f}".format(y[i]))
            self.tableWidget_4.item(i, 19).setText("{:0.2f}".format(y[i]))

        b = [sum([args_2[i][j] * y[i] / 32 for i in range(32)]) for j in range(22)]
        
        for i in range(32):
            self.tableWidget_3.item(i, 8).setText("{:0.4f}".format(sum([b[j] * \
                args_2[i][j] for j in range(7)])))
        
        for i in range(32):
            self.tableWidget_4.item(i, 20).setText("{:0.5f}".format(sum([b[j] * \
                args_2[i][j] for j in range(19)])))

        self.plainTextEdit_5.setPlainText("y = {:+0.4f} * x0 {:+0.4f} * x1 {:+0.4f} \
* x2 {:+0.4f} * x3 {:+0.4f} * x4 {:+0.4f} * x5 {:+0.4f} * x6".format(*b))
        self.plainTextEdit_6.setPlainText("y = {:+0.4f} * x0 {:+0.4f} * x1 {:+0.4f} \
* x2 {:+0.4f} * x3 {:+0.4f} * x4 {:+0.4f} * x5 {:+0.4f} * x6 {:+0.4f} * x1 * x2 \
{:+0.4f} * x1 * x3 {:+0.4f} * x1 * x4 {:+0.4f} * x1 * x5 \
{:+0.4f} * x1 * x6 {:+0.4f} * x2 * x3 {:+0.4f} * x2 * x4 {:+0.4f} * x2 * x5 \
{:+0.4f} * x2 * x6 {:+0.4f} * x3 * x4 {:+0.4f} * x3 * x5 {:+0.4f} *x3 * x6".format(*b))

    def ockp(self):
        requests = int(self.spinBox.value())
        lambda_1 = self.doubleSpinBox_11.value()
        lambda_2 = self.doubleSpinBox_12.value()
        mu_1 = self.doubleSpinBox_13.value()
        mu_2 = self.doubleSpinBox_14.value()
        sigma_1 = self.doubleSpinBox_15.value()
        sigma_2 = self.doubleSpinBox_16.value()

        lambda_3 = self.doubleSpinBox_17.value()
        lambda_4 = self.doubleSpinBox_18.value()
        mu_3 = self.doubleSpinBox_19.value()
        mu_4 = self.doubleSpinBox_27.value()
        sigma_3 = self.doubleSpinBox_28.value()
        sigma_4 = self.doubleSpinBox_29.value()
        
        l_b = (lambda_1 + lambda_2) / 2.0
        l_d = lambda_2 - l_b
        l_b2 = (lambda_3 + lambda_4) / 2.0
        l_d2 = lambda_4 - l_b2
        m_b = (mu_1 + mu_2) / 2.0
        m_d = mu_2 - m_b
        m_b2 = (mu_3 + mu_4) / 2.0
        m_d2 = mu_4 - m_b2
        s_b = (sigma_1 + sigma_2) / 2.0
        s_d = sigma_2 - s_b
        s_b2 = (sigma_3 + sigma_4) / 2.0
        s_d2 = sigma_4 - s_b2
        
        args = []
        for i in range(45):
            args.append([])
            for j in range(28):
                args[-1].append(float(self.tableWidget_7.item(i, j).text()))
        
        y = []
        for i in range(45):
            l = l_b + l_d * args[i][1]
            l2 = l_b2 + l_d2 * args[i][2]
            m = m_b + m_d * args[i][3]
            m2 = m_b2 + m_d2 * args[i][4]
            s = s_b + s_d * args[i][5]
            s2 = s_b2 + s_d2 * args[i][6]
        
            queued_mean = self.dt_principle(l, l2, m, m2, s, s2)
            
            y.append(queued_mean)
            self.tableWidget_7.item(i, 28).setText("{:0.4f}".format(queued_mean))
        
        a = [sum(y) / 45]
        
        for j in range(1, 7):
            a.append(sum([args[i][j] * y[i] for i in range(45)]) / 37.9473)
        
        for j in range(7, 22):
            a.append(sum([args[i][j] * y[i] for i in range(45)]) / 32)
        
        for j in range(22, 28):
            a.append(sum([args[i][j] * y[i] for i in range(45)]) / 17.6854)

        for i in range(45):
            self.tableWidget_7.item(i, 29).setText("{:0.4f}".format(sum([a[j] * args[i][j] for j in range(28)])))
        
        self.plainTextEdit_7.setPlainText("y = {:+0.4f} {:+0.4f} * x1 {:+0.4f} * x2 {:+0.4f} * x3 {:+0.4f} * x4 {:+0.4f} * x5 {:+0.4f} * x6 {:+0.4f} * x1 * x2 {:+0.4f} * x1 * x3 {:+0.4f} * x1 * x4 {:+0.4f} * x1 * x5 {:+0.4f} * x1 * x6 {:+0.4f} * x2 * x3 {:+0.4f} * x2 * x4 {:+0.4f} * x2 * x5 {:+0.4f} * x2 * x6 {:+0.4f} * x3 * x4 {:+0.4f} * x3 * x5 {:+0.4f} * x3 * x6 {:+0.4f} * x4 * x5 {:+0.4f} * x4 * x6 {:+0.4f} * x5 * x6 {:+0.4f} * (x1^2 − 0.8433) {:+0.4f} * (x2^2 − 0.8433) {:+0.4f} * (x3^2 − 0.8433) {:+0.4f} * (x4^2 − 0.8433) {:+0.4f} * (x5^2 − 0.8433) {:+0.4f} * (x6^2 − 0.8433)".format(*a))

        for i in range(45):
            print("{:+0.4f},{:+0.4f}".format(y[i], sum([a[j] * args[i][j] for j in range(28)])))

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
