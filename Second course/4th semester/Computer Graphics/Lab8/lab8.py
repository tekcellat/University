import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPainter,QColor,QPen,QCursor,QImage,QPixmap
from PyQt5.QtCore import Qt,QObject,QPoint
from SLGraphic import SLGraphicsScene
from mathmodule import *

WIDTH = 500
HIGHT = 480

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
        self.setWindowTitle('Отсечение отрезков')
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

        v1 = QHBoxLayout()
        
        self.clear = QPushButton('Очистить', self)
        self.clear.resize(self.fill_butt.sizeHint())
        v1.addWidget(self.clear)
        
        self.Add = QPushButton('Добавить', self)
        self.Add.resize(self.fill_butt.sizeHint())     
        v1.addWidget(self.Add)

        v2 = QVBoxLayout()

        self.rb1 = QRadioButton(self)
        self.rb1.setText("Ввод отрезков")

        self.rb2 = QRadioButton(self)
        self.rb2.setText("Ввод выпуклого отсекателя")
        self.rb2.setChecked(True)

        self.color_button = QPushButton(self)
        self.color_button1 = QPushButton(self)
        
      
        v2.addWidget(self.rb2)
        v2.addWidget(self.rb1)
        
        self.colormain = QColor(0,255,0).rgb()
        self.color_button.setStyleSheet('QPushButton{background-color:'+
                                        QColor(0,255,0).name()+'}')

        self.colorhelp = QColor(0,0,255).rgb()
        self.color_button1.setStyleSheet('QPushButton{background-color:'+
                                        QColor(0,0,255).name()+'}')

        self.infoTable = QTableWidget()
        self.infoTable.setColumnCount(2)
        self.infoTable.setHorizontalHeaderLabels(["x","y"])
        #self.infoTable.resizeColumnsToContents()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["x1","y1","x2","y2"])
        self.table.resizeColumnsToContents()

        self.tab = QTabWidget()
        self.tab.addTab(self.infoTable,"Отсекатель")
        self.tab.addTab(self.table,"Отрезки")

        self.v.addWidget(self.tab)
        self.v.addLayout(v1)
        self.v.addWidget(self.fill_butt)
        self.v.addLayout(v2)
        
        self.capslock = False

        self.color_button.clicked.connect(lambda: self.GetColor())
        self.color_button1.clicked.connect(lambda: self.GetColor1())
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
        self.color_button.setStyleSheet('QPushButton{background-color:'+
                                        hexcolor+'}')


    def GetColor1(self):
        color = QColorDialog.getColor()
        self.colorhelp = color.rgb()
        hexcolor = color.name()
        self.color_button1.setStyleSheet('QPushButton{background-color:'+
                                        hexcolor+'}')
        

    def cut_convex(self,edges,cutter):
        normVect = []
        d = get_direction(cutter)
        
        if d == 0:
            return
        
        norm_vecs(normVect, cutter, d)
        
        visible = True
        n = len(edges)
        
        for i in range(n):
            visible, p1, p2 = cut_line(cutter, normVect,
                     edges[i][:2]+[0],
                     edges[i][2:]+[0],
                     visible)
            
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

        convex_flag = check_convex(self.edges)
        if convex_flag == 0:
            self.ShowWarning("Заданный многоугольник вырожден в отрезок!")
            return
        elif convex_flag == -1:
            self.ShowWarning("Задан невыпуклый многоугольник!")
            return
        self.cut_convex(self.edges_slave, self.edges)

   
    def ShowDialog(self):
        if self.rb2.isChecked():
            text, ok = QInputDialog.getText(self, 'Ввод вершины',
                                        'Введите по типу X Y:')
            if self.cutter_flag:
                self.edges.clear()
                self.infoTable.setRowCount(0)
                self.image.fill(Qt.white)
                self.draw_borders()
                self.cutter_flag = False
                
            if ok:
                text = text.split()
                x = int(text[0])
                y = int(text[1])
                if len(self.edges) > 0:
                    self.Bresenham(self.edges[0][0],
                                   self.edges[0][1],
                                   x,y)
                self.edges.append([x,y,0])
                self.info_appender([x,y])
        else:
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
        self.infoTable.setRowCount(0)
        self.image.fill(Qt.white)


    def draw_borders(self):
        if len(self.edges_slave) != 0:
            for j in range(len(self.edges_slave)):
                self.Bresenham(self.edges_slave[j][0],
                               self.edges_slave[j][1],
                               self.edges_slave[j][2],
                               self.edges_slave[j][3],self.colorhelp)
        
        if len(self.edges) > 1:
            for i in range(len(self.edges)-1):
                self.Bresenham(self.edges[i][0],
                               self.edges[i][1],
                               self.edges[i+1][0],
                               self.edges[i+1][1])
        self.repaint()
        

    def mousePressEvent(self, QMouseEvent):
        if self.rb2.isChecked():
            if self.cutter_flag:
                self.edges.clear()
                self.infoTable.setRowCount(0)
                self.image.fill(Qt.white)
                self.draw_borders()
                
            if (QMouseEvent.button() == Qt.LeftButton):
                self.cutter_flag = False
                cord = QMouseEvent.pos()
                
                y = cord.y()
                x = cord.x()
                if (x >= 10 and y >= 10 and y <= HIGHT and x <= WIDTH):
                    x -= 10
                    y -= 10
                    i = len(self.edges)

                    if self.capslock and i:
                        if y != self.edges[i-1][1]:
                            der = ((x - self.edges[i-1][0])/
                                (y - self.edges[i-1][1]))
                        else:
                            der = 2
                        if abs(der) <= 1:
                            x = self.edges[i-1][0]
                        else:
                            y = self.edges[i-1][1]

                    if i:
                        self.Bresenham(self.edges[i-1][0],
                                       self.edges[i-1][1],
                                       x,y)
                    self.edges.append([x,y,0])
                    self.info_appender([x,y])                    
                    
            elif (QMouseEvent.button() == Qt.RightButton):
                i = len(self.edges)
                if i:
                    x = self.edges[0][0]
                    y = self.edges[0][1]
                    self.Bresenham(self.edges[i-1][0],
                                   self.edges[i-1][1],
                                   x,y)
                    self.edges.append([x,y,0])
                    self.cutter_flag = True
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


    def info_appender(self,cord):
        N = self.infoTable.rowCount()
        self.infoTable.setRowCount(N+1)
        for i in range(len(cord)):
            self.infoTable.setItem(N,i,QTableWidgetItem(str(cord[i])))


    def paintEvent(self, e):
        self.scene.clear()
        self.scene.addPixmap(QPixmap.fromImage(self.image))

                     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = Example()   
    MainWindow.show()        
    sys.exit(app.exec_())
