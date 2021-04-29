import sys

from PyQt5.QtWidgets import QApplication

from mywindow import MyWindow

if __name__ == '__main__':
    app = QApplication([])
    application = MyWindow()
    application.show()

    sys.exit(app.exec())
