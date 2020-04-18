import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPainter,QColor,QPen,QCursor,QImage,QPixmap
from PyQt5.QtCore import Qt,QObject,QPoint
from math import tan
from SLGraphic import SLGraphicsScene
from mathmodule import *

WIDTH = 500
HIGHT = 480

def sign(x):
    return int((x > 0) - (x < 0))
	

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.edges = []       # отсекатель
        self.edges_slave = [] # отрезки
        self.one_slave = []


    def Bresenham(self,x1,y1,x2,y2,color = QColor(0,0,0).rgb(),t=False):
            dx = int(x2 - x1)
            dy = int(y2 - y1)
            sx = sign(dx)
            sy = sign(dy)
            dx = abs(dx)
            dy = abs(dy)    

            swap = False
            if (dy <= dx):
                swap = False
            else:
                swap = True
                dx,dy = dy,dx
        
    
            e = int(2*dy-dx)
            x = int(x1)
            y = int(y1)
            
            for i in range(dx+1):
                self.image.setPixel(x,y,color)
                if t:
                    self.image.setPixel(x+1,y,color)
                    self.image.setPixel(x-1,y,color)
                    self.image.setPixel(x,y+1,color)
                    self.image.setPixel(x,y-1,color)
                if (e>=0):
                    if (swap):
                        x += sx
                    else:
                        y +=sy
                    e = e-2*dx
                if (e < 0): 
                    if (swap):
                        y +=sy
                    else:
                        x += sx
                    e = e+2*dy

                    
    def initUI(self):
        self.cutter_flag = False
        self.setGeometry(100,100, 800, 500)
        self.setWindowTitle('Возможно здесь должен быть заголовок - Отсечение отрезков')
        self.Group = QHBoxLayout(self)
        self.v = QVBoxLayout()
        self.GraphView = QGraphicsView(self)
        self.GraphView.setCursor(Qt.CrossCursor)
        self.GraphView.setMouseTracking(True)
        
        self.scene = SLGraphicsScene(self)
        self.image = QImage(WIDTH,HIGHT - 20,QImage.Format_RGB32)

        self.Group.addWidget(self.GraphView)
        self.Group.addLayout(self.v)
        self.image.fill(Qt.white)
        

        self.GraphView.setGeometry(10,10,WIDTH,HIGHT )
        self.GraphView.setStyleSheet("background-color: white")
        self.scene.addPixmap(QPixmap.fromImage(self.image))

        self.GraphView.setScene(self.scene)        

        self.fill_butt = QPushButton('Выполнить отсечение', self)
        self.fill_butt.resize(self.fill_butt.sizeHint())

        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["x1","y1","x2","y2"])
        self.table.resizeColumnsToContents()
        self.v.addWidget(self.table)

        v1 = QHBoxLayout()
        
        self.clear = QPushButton('Очистить', self)
        self.clear.resize(self.fill_butt.sizeHint())
        v1.addWidget(self.clear)
        
        self.Add = QPushButton('Добавить', self)
        self.Add.resize(self.fill_butt.sizeHint())     
        v1.addWidget(self.Add)
        self.v.addLayout(v1)
        self.v.addWidget(self.fill_butt)

        v2 = QVBoxLayout()
        self.v.addLayout(v2)

        self.rb1 = QRadioButton(self)
        self.rb1.setText("Ввод отрезков")

        self.rb2 = QRadioButton(self)
        self.rb2.setText("Ввод регулярного отсекателя")
        self.rb2.setChecked(True)

        self.color_button = QPushButton(self)
        self.color_button1 = QPushButton(self)
        
    
        v2.addWidget(self.rb2)
        v2.addWidget(self.rb1)
        
        self.colormain = QColor(0,255,0).rgb()
      

        self.colorhelp = QColor(0,0,255).rgb()
       
        self.infoLabel = QLabel(self)
        self.infoLabel.setText("")
        v2.addWidget(self.infoLabel)
        
        self.capslock = False

        self.Add.clicked.connect(lambda: self.ShowDialog())
        self.fill_butt.clicked.connect(lambda: self.Cut())
        self.clear.clicked.connect(lambda: self.Clear())
        self.show()
    

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == 16777252:
            self.capslock = not self.capslock
    

    def GetColor(self):
        color = QColorDialog.getColor()
        self.colormain = color.rgb()
        hexcolor = color.name()



    def GetColor1(self):
        color = QColorDialog.getColor()
        self.colorhelp = color.rgb()
        hexcolor = color.name()



    def cut_regular(self,edges,cutter):
        sort_cutter(cutter)
        
        xl = cutter[0][0]
        yu = cutter[1][1]
        xr = cutter[1][0]
        yd = cutter[0][1]
        
        n = len(edges)
        visible = True
        
        for i in range(n):
            visible, p1, p2 = easy_cut(xl,xr,yd,yu,
                     edges[i][:2],
                     edges[i][2:])

            if visible:
                self.Bresenham(p1[0], p1[1],
                               p2[0], p2[1],
                               self.colormain,
                               True)


    def Cut(self):
        self.draw_borders()

        if len(self.edges) == 0:
            self.ShowWarning("Не задан отсекатель!")
            return
        elif len(self.edges_slave) == 0:
            self.ShowWarning("Не задан ни один отрезок!")
            return

        self.cut_regular(self.edges_slave, self.edges)

   
    def ShowDialog(self):
        text, ok = QInputDialog.getText(self, 'Ввод отрезка',
                                        'Введите по типу X1 Y1 X2 Y2:')
        if ok:
            text = text.split()
            x1 = int(text[0])
            y1 = int(text[1])
            x2 = int(text[2])
            y2 = int(text[3])
            self.Bresenham(x1,y1,x2,y2,self.colorhelp)
            self.edges_slave.append([x1,y1,x2,y2])
            self.table_appender([x1,y1,x2,y2])


    def ShowWarning(self, info):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)

        msg.setText(info+"\nНевозможно провести отсечение!")
        msg.setWindowTitle("Внимание!")
        msg.exec_()


    def Clear(self):
        self.edges.clear()
        self.edges_slave.clear()
        self.table.setRowCount(0)
        self.image.fill(Qt.white)
        self.infoLabel.setText("")


    def draw_borders(self):
        if len(self.edges_slave) != 0:
            for j in range(len(self.edges_slave)):
                self.Bresenham(self.edges_slave[j][0],
                               self.edges_slave[j][1],
                               self.edges_slave[j][2],
                               self.edges_slave[j][3],self.colorhelp)
                
        if len(self.edges) > 1:
            self.Bresenham(self.edges[0][0],
                           self.edges[0][1],
                           self.edges[1][0],
                           self.edges[0][1])
            self.Bresenham(self.edges[1][0],
                           self.edges[0][1],
                           self.edges[1][0],
                           self.edges[1][1])
            self.Bresenham(self.edges[1][0],
                           self.edges[1][1],
                           self.edges[0][0],
                           self.edges[1][1])
            self.Bresenham(self.edges[0][0],
                           self.edges[1][1],
                           self.edges[0][0],
                           self.edges[0][1])
            sort_cutter(self.edges)
            text = "Отсекатель (л.в. точка, пр.н. точка):\n"
            self.infoLabel.setText(text+str(self.edges[0])+' ; '+str(self.edges[1]))
        self.repaint()
        

    def mousePressEvent(self, QMouseEvent):
        if self.rb2.isChecked():
            if (QMouseEvent.button() == Qt.LeftButton):
                if len(self.edges) == 1:
                    self.cutter_flag = True
                else:
                    self.cutter_flag = False

                cord = QMouseEvent.pos()
                
                y = cord.y()
                x = cord.x()
                if (x >= 10 and y>=10 and y<=HIGHT and x<=WIDTH):
                    x -= 10
                    y -= 10
                    i = len(self.edges)
                    if i >= 2:
                        self.edges.clear()
                        self.infoLabel.setText("")

                    self.edges.append([x,y,0])
                                           
                self.image.fill(Qt.white)
                self.draw_borders()
                    
        elif self.rb1.isChecked(): # Input lines
            if (QMouseEvent.button() == Qt.LeftButton):
                cord = QMouseEvent.pos()
                
                y = cord.y()
                x = cord.x()
                if (x >= 10 and y>=10 and y<=HIGHT and x<=WIDTH):
                    x -= 10
                    y -= 10
                    i = len(self.one_slave)
                    
                    if self.capslock and i:
                        if y != self.one_slave[1]:
                            der = ((x - self.one_slave[0])/
                                   (y - self.one_slave[1]))
                        else:
                            der = 2
                        if abs(der) <= 1:
                            x = self.one_slave[0]
                        else:
                            y = self.one_slave[1]
                            
                    if i == 2:
                        self.one_slave.append(x)
                        self.one_slave.append(y)
                        self.edges_slave.append(self.one_slave)
                        self.table_appender(self.one_slave)
                        self.one_slave = []
                    else:
                        self.one_slave.append(x)
                        self.one_slave.append(y)

                self.image.fill(Qt.white)
                self.draw_borders()


    def table_appender(self,cord):
        N = self.table.rowCount()
        self.table.setRowCount(N+1)
        for i in range(len(cord)):
            self.table.setItem(N,i,QTableWidgetItem(str(cord[i])))


    def paintEvent(self, e):
        self.scene.clear()
        self.scene.addPixmap(QPixmap.fromImage(self.image))

                     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = Example()   
    MainWindow.show()        
    sys.exit(app.exec_())
