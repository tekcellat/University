import sys,copy
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPainter,QColor,QPen,QCursor,QImage,QPixmap
from PyQt5.QtCore import Qt,QObject,QPoint
from math import tan

WIDTH = 500
HIGHT = 480

edges = []
edges_slave = []

def sign(x):
    if (x > 0):
        return 1
    elif (x < 0):
        return -1
    else:
        return 0
        

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        

    def fill_zatravka(self,x_zatravka,y_zatravka):
        stack = [[x_zatravka,y_zatravka]]
        fill_color  = self.colormain
        line_color = QColor(0,0,0)
        line_color = line_color.rgb()
        while (len(stack)):
            QApplication.processEvents()
            x,y = stack.pop()
            self.image.setPixel(x,y,fill_color)
            temp_x = x

            while(self.image.pixelColor(x,y).rgb() != line_color):
                self.image.setPixel(x,y,fill_color)
                x +=1 
            x_prav = x - 1

            x = temp_x
            while(self.image.pixelColor(x,y).rgb() != line_color):
                self.image.setPixel(x,y,fill_color)
                x -=1
                
            self.repaint()

            x_lev = x + 1

            x = x_lev
            y += 1
            while(x <=x_prav):
                flag = False
                while(self.image.pixelColor(x,y).rgb() != line_color and self.image.pixelColor(x,y).rgb() != fill_color and x <= x_prav ):
                    if flag == False:
                        flag = True
                    x += 1

                if flag == True:
                    if (self.image.pixelColor(x,y).rgb() != line_color and self.image.pixelColor(x,y).rgb() != fill_color and x == x_prav ):
                        stack.append([x,y])
                    else:
                        stack.append([x-1,y])
                    flag = False

                x_vhod = x
                while(self.image.pixelColor(x,y).rgb() != line_color and self.image.pixelColor(x,y).rgb() != fill_color and x < x_prav ):
                    x += 1

                if x == x_vhod:
                    x += 1
            x = x_lev
            y -= 2
            #Second part
            while(x <=x_prav):
                flag = False
                while(self.image.pixelColor(x,y).rgb() != line_color and self.image.pixelColor(x,y).rgb() != fill_color and x <= x_prav ):
                    if flag == False:
                        flag = True
                    x += 1

                if flag == True:
                    if (self.image.pixelColor(x,y).rgb() != line_color and self.image.pixelColor(x,y).rgb() != fill_color and x == x_prav ):
                        stack.append([x,y])
                    else:
                        stack.append([x-1,y])
                    flag = False

                x_vhod = x
                while(self.image.pixelColor(x,y).rgb() != line_color and self.image.pixelColor(x,y).rgb() != fill_color and x < x_prav ):
                    x += 1

                if x == x_vhod:
                    x += 1


    def Bresenham(self,x1,y1,x2,y2,color = QColor(0,0,0).rgb()):
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

                    
    def CMidpoint(self):
        fill_color = QColor(0,0,0).rgb()
        xc = int(self.zpx.text())
        yc = int(self.zpy.text())
        R = 50

        p = int(1 - R)
        x = 0
        y = R

        self.image.setPixel(int(xc + x),int(yc + y),fill_color)
        self.image.setPixel(int(xc + x),int(yc - y),fill_color)
        self.image.setPixel(int(xc - x),int(yc + y),fill_color)
        self.image.setPixel(int(xc - x),int(yc - y),fill_color)
        self.image.setPixel(int(xc + y),int(yc + x),fill_color)
        self.image.setPixel(int(xc + y),int(yc - x),fill_color)
        self.image.setPixel(int(xc - y),int(yc + x),fill_color)
        self.image.setPixel(int(xc - y),int(yc - x),fill_color)

        while(x < y):
            x += 1
            if (p < 0):
                p += 2*x + 1
            else:
                y -= 1
                p += 2*(x-y) + 1

            self.image.setPixel(int(xc + x),int(yc + y),fill_color)
            self.image.setPixel(int(xc + x),int(yc - y),fill_color)
            self.image.setPixel(int(xc - x),int(yc + y),fill_color)
            self.image.setPixel(int(xc - x),int(yc - y),fill_color)
            self.image.setPixel(int(xc + y),int(yc + x),fill_color)
            self.image.setPixel(int(xc + y),int(yc - x),fill_color)
            self.image.setPixel(int(xc - y),int(yc + x),fill_color)
            self.image.setPixel(int(xc - y),int(yc - x),fill_color)


    def initUI(self):      
        self.setGeometry(100,100, 800, 500)
        self.setWindowTitle('Points')
        self.Group = QHBoxLayout(self)
        self.v = QVBoxLayout()
        self.GraphView = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.image = QImage(WIDTH,HIGHT - 20,QImage.Format_RGB32)

        self.Group.addWidget(self.GraphView)
        self.Group.addLayout(self.v)
        self.image.fill(Qt.white)
        

        self.GraphView.setGeometry(10,10,WIDTH,HIGHT )
        self.GraphView.setStyleSheet("background-color: white")
        self.scene.addPixmap(QPixmap.fromImage(self.image))


        self.GraphView.setScene(self.scene)        

        self.fill_butt = QPushButton('Fill', self)
        self.fill_butt.resize(self.fill_butt.sizeHint())

        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["x","y"])
        self.v.addWidget(self.table)

        v1 = QHBoxLayout()
        
        self.clear = QPushButton('Clear', self)
        self.clear.resize(self.fill_butt.sizeHint())
        v1.addWidget(self.clear)
        
        self.Add = QPushButton('Add', self)
        self.Add.resize(self.fill_butt.sizeHint())     
        v1.addWidget(self.Add)
        self.v.addLayout(v1)
        self.v.addWidget(self.fill_butt)

        v2 = QVBoxLayout()
        v3 = QHBoxLayout()
        v4 = QHBoxLayout()
        self.v.addLayout(v2)
        self.zplbl = QLabel(self)
        self.zplbl.setText("The seed pixel:")

        self.zpx = QLineEdit(self)
        self.zpx.setText("0")
        
        self.zpxlbl = QLabel(self)
        self.zpxlbl.setText("X = ")
        v3.addWidget(self.zpxlbl)
        v3.addWidget(self.zpx)
        
        self.zpy = QLineEdit(self)
        self.zpy.setText("0")
        
        self.zpylbl = QLabel(self)
        self.zpylbl.setText("Y = ")
        v4.addWidget(self.zpylbl)
        v4.addWidget(self.zpy)

        self.rb3 = QRadioButton(self)
        self.rb3.setText("Choosing seed")

        self.rb2 = QRadioButton(self)
        self.rb2.setText("Progressive seed algorithm")
        self.rb2.setChecked(True)

       
        v2.addWidget(self.rb2)
        v2.addWidget(self.rb3)
        v2.addWidget(self.zplbl)
        v2.addLayout(v3)
        v2.addLayout(v4)
        
        self.colormain = QColor(0,255,0).rgb()
        self.capslock = False


        self.Add.clicked.connect(lambda: self.ShowDialog())
        self.fill_butt.clicked.connect(lambda: self.Fill())
        self.clear.clicked.connect(lambda: self.Clear())
        self.show()
    

    def keyPressEvent(self, QKeyEvent):
        if (QKeyEvent.key() == 67 or QKeyEvent.key() == 99):
            self.CMidpoint()
        elif QKeyEvent.key() == 16777252:
            self.capslock = not self.capslock
    

    def GetColor(self):
        color = QColorDialog.getColor()
        self.colormain = color.rgb()
        hexcolor = color.name()
        self.color_button.setStyleSheet('QPushButton{background-color:'+hexcolor+'}')


    def Fill(self):
        self.draw_borders()
        x_zatr = int(self.zpx.text())
        y_zatr = int(self.zpy.text())
        self.fill_zatravka(x_zatr,y_zatr)


   
    def ShowDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter X Y:')
        if ok:
            text = text.split()
            x = int(text[0])
            y = int(text[1])
            i = len(edges_slave)
            if i:
                self.Bresenham(edges_slave[i-1][0],edges_slave[i-1][1],x,y)
            edges_slave.append([x,y])
            self.table_appender([x,y])


    def Clear(self):
        edges.clear()
        edges_slave.clear()
        self.table.setRowCount(0)
        self.image.fill(Qt.white)


    def draw_borders(self):
        for j in range(len(edges)):
            for i in range(len(edges[j])-1):
                self.Bresenham(edges[j][i][0],edges[j][i][1],edges[j][i+1][0],edges[j][i+1][1])
        self.repaint()
        

    def mousePressEvent(self, QMouseEvent):
        if (QMouseEvent.button() == Qt.LeftButton):
            cord = QMouseEvent.pos()
            if self.rb3.isChecked():
                y = cord.y()
                x = cord.x()
                self.zpx.setText(str(x-10))
                self.zpy.setText(str(y-10))
                return
            
            y = cord.y()
            x = cord.x()
            if (x >= 10 and y>=10 and y<=HIGHT and x<=WIDTH):
                x -= 10
                y -= 10
                i = len(edges_slave)

                if self.capslock and i:
                    if y != edges_slave[i-1][1]:
                        der = (x - edges_slave[i-1][0])/(y - edges_slave[i-1][1])
                    else:
                        der  = 2
                    if abs(der) <= 1:
                        x = edges_slave[i-1][0]
                    else:
                        y = edges_slave[i-1][1]

                if i:
                    self.Bresenham(edges_slave[i-1][0],edges_slave[i-1][1],x,y)
                edges_slave.append([x,y])
                self.table_appender([x,y])

                
        elif (QMouseEvent.button() == Qt.RightButton):
            i = len(edges_slave)
            if i:
                x = edges_slave[0][0]
                y = edges_slave[0][1]
                self.Bresenham(edges_slave[i-1][0],edges_slave[i-1][1],x,y)
                edges_slave.append([x,y])
            edges.append(copy.deepcopy(edges_slave))
            edges_slave.clear()
            self.table_appender(['end','end'])
            
        elif QMouseEvent.button() == Qt.MiddleButton:
            cord = QMouseEvent.pos()
            y = cord.y()
            x = cord.x()
            self.zpx.setText(str(x-10))
            self.zpy.setText(str(y-10))


    def table_appender(self,coord):
        N = self.table.rowCount()
        self.table.setRowCount(N+1)
        self.table.setItem(N,0,QTableWidgetItem(str(coord[0])))
        self.table.setItem(N,1,QTableWidgetItem(str(coord[1])))


    def paintEvent(self, e):
        self.scene.clear()
        self.scene.addPixmap(QPixmap.fromImage(self.image))

                     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = Example()   
    MainWindow.show()        
    sys.exit(app.exec_())
