from PyQt5 import uic
from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import QMainWindow, QLineEdit
from fp_tables import *
from validentry import *


class FPMainWindow(QMainWindow):
    def __init__(self):
        super(FPMainWindow, self).__init__()
        uic.loadUi('fp_mainwindow.ui', self)

        self.btn_calculate.clicked.connect(self.calculate)

        self.show()

    @staticmethod
    def check_lang_percent(percents: dict):
        eps = 1e-7
        return abs(sum(percents.values()) - 100) < eps

    def get_lang_percents(self):
        res = {
            'ASM': get_valid(self.entry_percent_asm, float, lambda val: val < 0 or val > 100),
            'C': get_valid(self.entry_percent_c, float, lambda val: val < 0 or val > 100),
            'Cobol': get_valid(self.entry_percent_cobol, float, lambda val: val < 0 or val > 100),
            'Fortran': get_valid(self.entry_percent_fortran, float, lambda val: val < 0 or val > 100),
            'Pascal': get_valid(self.entry_percent_pascal, float, lambda val: val < 0 or val > 100),
            'CPP': get_valid(self.entry_percent_cpp, float, lambda val: val < 0 or val > 100),
            'Java': get_valid(self.entry_percent_java, float, lambda val: val < 0 or val > 100),
            'CSharp': get_valid(self.entry_percent_cs, float, lambda val: val < 0 or val > 100),
            'Ada': get_valid(self.entry_percent_ada, float, lambda val: val < 0 or val > 100),
            'SQL': get_valid(self.entry_percent_sql, float, lambda val: val < 0 or val > 100),
            'VCPP': get_valid(self.entry_percent_vcpp, float, lambda val: val < 0 or val > 100),
            'Delphi': get_valid(self.entry_percent_delphi, float, lambda val: val < 0 or val > 100),
            'Perl': get_valid(self.entry_percent_perl, float, lambda val: val < 0 or val > 100),
            'Prolog': get_valid(self.entry_percent_prolog, float, lambda val: val < 0 or val > 100),
        }
        entries = self.findChildren(QLineEdit, QRegExp("entry_percent_"))
        if not self.check_lang_percent(res):
            for entry in entries:
                make_invalid(entry)
            raise ValueError
        else:
            for entry in entries:
                make_valid(entry)
        return res

    def get_fp_total(self):
        fp = 0
        fp += get_valid(self.entry_ilf, int, lambda val: val < 0) * levels['ILF'][self.cb_ilf.currentIndex()]
        fp += get_valid(self.entry_eif, int, lambda val: val < 0) * levels['EIF'][self.cb_eif.currentIndex()]
        fp += get_valid(self.entry_ei, int, lambda val: val < 0) * levels['EI'][self.cb_ei.currentIndex()]
        fp += get_valid(self.entry_eo, int, lambda val: val < 0) * levels['EO'][self.cb_eo.currentIndex()]
        fp += get_valid(self.entry_eq, int, lambda val: val < 0) * levels['EQ'][self.cb_eq.currentIndex()]
        return fp

    def get_sysparams(self):
        res = list()
        for i in range(1, 15):
            entry = self.findChild(QLineEdit, "entry_param" + str(i))
            res.append(get_valid(entry, int, lambda val: val < 0 or val > 5))
        return res

    def calculate(self):
        try:
            FP = self.get_fp_total()
            params = self.get_sysparams()
            percents = self.get_lang_percents()

            self.label_fp_total.setText(str(FP))

            FP *= (0.65 + 0.01 * sum(params))
            self.label_fp_corrected.setText(str(round(FP, 3)))

            loc = 0
            for lang in percents.items():
                loc += FP * fp_to_loc[lang[0]] * lang[1] / 100
            loc = round(loc)
            self.label_loc.setText(str(loc))

        except ValueError:
            pass
