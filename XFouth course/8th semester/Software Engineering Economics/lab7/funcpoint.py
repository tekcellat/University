import sys
from PyQt5.QtWidgets import QApplication
from fp_mainwindow import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FPMainWindow()
    sys.exit(app.exec_())
