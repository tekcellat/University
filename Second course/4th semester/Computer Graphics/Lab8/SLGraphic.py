from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

WIDTH = 500
HIGHT = 480

class SLGraphicsScene(QGraphicsScene):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent


    def mouseMoveEvent(self, event):
        parent = self.parent
        if parent.rb2.isChecked():
            parent.image.fill(Qt.white)
            parent.draw_borders()

            cord = event.scenePos()
            
            x = cord.x()
            y = cord.y()
            if (x >= 10 and y >= 10 and y <= HIGHT and x <= WIDTH):
                x += 2
                y += 10
                num = len(parent.edges)
                
                if num > 0 and not parent.cutter_flag:
                    parent.image.fill(Qt.white)
                    parent.draw_borders()
                    parent.Bresenham(parent.edges[num-1][0],
                                     parent.edges[num-1][1],
                                     x,y)

        if parent.rb1.isChecked():
            parent.image.fill(Qt.white)
            parent.draw_borders()

            cord = event.scenePos()
            
            x = cord.x()
            y = cord.y()
            if (x >= 10 and y >= 10 and y <= HIGHT and x <= WIDTH):
                x += 2
                y += 10
                num = len(parent.one_slave)
                
                if num > 0:
                    parent.image.fill(Qt.white)
                    parent.draw_borders()
                    parent.Bresenham(parent.one_slave[0],
                                     parent.one_slave[1],
                                     x,y,parent.colorhelp)


if __name__ == "__main__":
    pass
