from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
# from c2_tables import *
from validentry import *


project_params = {
    "PREC": [6.2, 4.96, 3.72, 2.48, 1.24, 0.0],
    "FLEX": [5.07, 4.05, 3.04, 2.03, 1.01, 0.0],
    "RESL": [7.07, 5.65, 4.24, 2.83, 1.41, 0.0],
    "TEAM": [5.48, 4.38, 3.29, 2.19, 1.10, 0.0],
    "PMAT": [7.8, 6.24, 4.68, 3.12, 1.56, 0.0]
}

arch_params = {
    "PERS": [1.62, 1.26, 1.00, 0.83, 0.63, 0.50],
    "RCPX": [0.60, 0.83, 1.00, 1.33, 1.91, 2.72],
    "RUSE": [0.95, 1.00, 1.07, 1.15, 1.24],
    "PDIF": [0.87, 1.00, 1.29, 1.81, 2.61],
    "PREX": [1.33, 1.22, 1.00, 0.87, 0.74, 0.62],
    "FCIL": [1.30, 1.10, 1.00, 0.87, 0.73, 0.62],
    "SCED": [1.43, 1.14, 1.00, 1.00, 1.00]
}

speed_levels = [4, 7, 13, 25, 50]




class C2MainWindow(QMainWindow):
    def __init__(self):
        super(C2MainWindow, self).__init__()
        uic.loadUi("c2_mainwindow.ui", self)

        self.btn_calculate.clicked.connect(self.calculate)

        self.show()

    def get_p(self):
        res = 101  # 1.01 * 100
        res += project_params["PREC"][self.cb_prec.currentIndex()]
        res += project_params["FLEX"][self.cb_flex.currentIndex()]
        res += project_params["RESL"][self.cb_resl.currentIndex()]
        res += project_params["TEAM"][self.cb_team.currentIndex()]
        res += project_params["PMAT"][self.cb_pmat.currentIndex()]
        return res / 100

    def get_op(self):
        res = get_valid(self.entry_forms_simple, int, lambda val: val < 0)
        res += 2 * get_valid(self.entry_forms_moderate, int, lambda val: val < 0)
        res += 3 * get_valid(self.entry_forms_complex, int, lambda val: val < 0)
        res += 2 * get_valid(self.entry_reports_simple, int, lambda val: val < 0)
        res += 5 * get_valid(self.entry_reports_moderate, int, lambda val: val < 0)
        res += 8 * get_valid(self.entry_reports_complex, int, lambda val: val < 0)
        res += 10 * get_valid(self.entry_modules, int, lambda val: val < 0)
        return res

    def get_earch(self):
        res = 1
        res *= arch_params["PERS"][self.cb_pers.currentIndex()]
        res *= arch_params["RCPX"][self.cb_rcpx.currentIndex()]
        res *= arch_params["RUSE"][self.cb_ruse.currentIndex()]
        res *= arch_params["PDIF"][self.cb_pdif.currentIndex()]
        res *= arch_params["PREX"][self.cb_prex.currentIndex()]
        res *= arch_params["FCIL"][self.cb_fcil.currentIndex()]
        res *= arch_params["SCED"][self.cb_sced.currentIndex()]
        return res

    def calculate(self):
        try:
            p = self.get_p()
            op = self.get_op()
            prod = speed_levels[self.cb_speed.currentIndex()]
            reuse = get_valid(self.entry_reuse, float, lambda val: val < 0 or val > 100)
            size = get_valid(self.entry_kloc, int, lambda val: val < 1)
            salary = get_valid(self.entry_salary, int, lambda val: val < 0)

            lc_comp = op * (100 - reuse) / (100 * prod)
            time_comp = 3 * lc_comp ** (0.33 + 0.2 * (p - 1.01))
            budget_comp = salary * lc_comp * time_comp

            lc_arch = 2.45 * self.get_earch() * size ** p
            time_arch = 3 * lc_arch ** (0.33 + 0.2 * (p - 1.01))
            budget_arch = salary * lc_arch * time_arch

            accuracy = 3
            self.label_lc_comp.setText(str(round(lc_comp, accuracy)))
            self.label_time_comp.setText(str(round(time_comp, accuracy)))
            self.label_budget_comp.setText(str(round(budget_comp, accuracy)))
            self.label_lc_arch.setText(str(round(lc_arch, accuracy)))
            self.label_time_arch.setText(str(round(time_arch, accuracy)))
            self.label_budget_arch.setText(str(round(budget_arch, accuracy)))

        except ValueError:
            pass
