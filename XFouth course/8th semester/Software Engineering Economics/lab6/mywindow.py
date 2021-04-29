from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMainWindow, QTableWidgetItem

from lab6 import simple_expirement, standart_eaf, graphs


class MyWindow(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("window.ui", self)

        self.StartWorkButton.clicked.connect(lambda: self.startWork())
        self.GraphButton.clicked.connect(lambda: self.drawGraph())

    def startWork(self):
        eaf = standart_eaf
        eaf['RELY'] = float(self.RELYComboBox.currentText())
        eaf['DATA'] = float(self.DATAComboBox.currentText())
        eaf['CPLX'] = float(self.CPLXComboBox.currentText())
        eaf['TIME'] = float(self.TIMEComboBox.currentText())
        eaf['STOR'] = float(self.STORComboBox.currentText())
        eaf['VIRT'] = float(self.VIRTComboBox.currentText())
        eaf['TURN'] = float(self.TURNComboBox.currentText())
        eaf['ACAP'] = float(self.ACAPComboBox.currentText())
        eaf['AEXP'] = float(self.AEXPComboBox.currentText())
        eaf['PCAP'] = float(self.PCAPComboBox.currentText())
        eaf['VEXP'] = float(self.VEXPComboBox.currentText())
        eaf['LEXP'] = float(self.LEXPComboBox.currentText())
        eaf['MODP'] = float(self.MODPComboBox.currentText())
        eaf['TOOL'] = float(self.TOOLComboBox.currentText())
        eaf['SCED'] = float(self.SCEDComboBox.currentText())

        code_size = int(self.SizeSpinBox.value())
        basic_salary =  int(self.SalarySpinBox.value())
        mode = 'normal'
        if self.NormalRadioButton.isChecked():
            mode = 'normal'
        elif self.InterRadioButton.isChecked():
            mode = 'inter'
        elif self.InbuildRadioButton.isChecked():
            mode = 'inbuild'
        print(mode)

        result = simple_expirement(eaf, code_size, mode, basic_salary)
        print(result)

        self.WorkWithoutLineEdit.setText(str(result['work']))
        self.TimeWithoutLineEdit.setText(str(result['time']))

        plan_work = result['work'] + result['works_t'][0]
        plan_time = result['time'] + result['times_t'][0]

        self.WorkWithLineEdit.setText(str(plan_work))
        self.TimeWithLineEdit.setText(str(plan_time))
        self.CostLineEdit.setText(str(result['budget']))

        for i in range(len(result['works_t'])):
            el = result['works_t'][i]
            self.TraditionTable.setItem(i, 0, QTableWidgetItem(str('{:.3g}'.format(el))))
        for i in range(len(result['times_t'])):
            el = result['times_t'][i]
            self.TraditionTable.setItem(i, 1, QTableWidgetItem(str('{:.3g}'.format(el))))
        for i in range(len(result['workers'])):
            el = result['workers'][i]
            self.TraditionTable.setItem(i, 2, QTableWidgetItem(str(el)))
        for i in range(len(result['works'])):
            el = result['works'][i]
            self.WbsTable.setItem(i, 0, QTableWidgetItem(str('{:.3g}'.format(el))))

    def drawGraph(self):
        graphs()
