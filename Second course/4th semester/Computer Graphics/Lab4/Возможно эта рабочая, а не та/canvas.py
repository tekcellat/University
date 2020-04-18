from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from drawmodule import drawcircle

class Canvas(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.initUI()
        self.parent = parent
        self.type = 0

    def initUI(self):
        
        self.show()

    def paintEvent(self, e):

        painter = QPainter()
        
        painter.begin(self)

        painter.setPen(self.parent.back_color)
        painter.setBrush(self.parent.back_color)
        painter.drawRect(0,0,self.width(),self.height())
        
        drawcircle(painter, self.parent.circles,
                   self.parent.ellipses, self.type)
        
        painter.end()
        
        self.update()
