import sys
from PyQt5.QtWidgets import QApplication
from c2_mainwindow import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = C2MainWindow()
    sys.exit(app.exec_())
