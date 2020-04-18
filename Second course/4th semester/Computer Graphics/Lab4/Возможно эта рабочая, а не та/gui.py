import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from drawmodule import drawcircle
from math import pi,sin,cos
from canvas import Canvas

MAX_W = 500
MAX_H = 500

class Example(QWidget):
    def __init__(self):
        super().__init__()
        
        self.size = 1
        self.color = QColor(0,0,0,255)
        self.back_color = QColor(255,255,255)
        self.draw_back = False
        
        self.xc1 = 250
        self.yc1 = 250
        self.a = 50
        self.b = 20
        self.da = 50

        self.xc2 = 250
        self.yc2 = 250
        self.R = 50
        self.dr = 50

        self.step = 1
        
        self.draw_type = 0
        self.type = 0
        # Костыли
        self.flag = [[True, True, True, True, True],
                     [True, True, True, True], True]
        self.ellipses = []     # ellipses
        self.circles = []
        
        self.initUI()


    def initUI(self):

        self.setWindowTitle('DrawEllipse')
        
        Window = QHBoxLayout(self)

        # For drawing
        self.Canv = Canvas(self)
        self.Canv.setMinimumSize(MAX_W,MAX_H)

        # Left side widget
        self.Buttons = QWidget()
        self.Buttons.setFixedSize(200,500)

        self.initButtonsUI()

        # Packing sides
        Window.addWidget(self.Canv)
        Window.addWidget(self.Buttons)
        
        self.show()
    

    def initButtonsUI(self):
        Group1 = QVBoxLayout(self.Buttons)

        # Checkbox
        checkbox = QCheckBox('Рисовать фоном')
        #checkbox.toggle()
        checkbox.stateChanged.connect(self.changeColorToBack)

        # Checkbox
        checkbox1 = QCheckBox('Концентрическое рисование')
        #checkbox.toggle()
        checkbox1.stateChanged.connect(self.chooseDrawType)
        
        # Buttons
        h1 = QHBoxLayout()
        DrawButton = QPushButton("Нарисовать")
        ClearButton = QPushButton("Очистить")
        DrawButton.clicked.connect(self.add_ellipse)
        ClearButton.clicked.connect(self.clear)
        h1.addWidget(DrawButton)
        h1.addWidget(ClearButton)

        # Size input
        AGroup = QHBoxLayout()
        lbl_1 = QLabel("Size(1-20):")
        e1 = QLineEdit()
        e1.setValidator(QIntValidator(1,20))
        e1.setAlignment(Qt.AlignRight)
        e1.setFont(QFont("Arial",12))
        e1.setText("1")
        e1.textChanged.connect(self.textchanged50)

        AGroup.addWidget(lbl_1)
        AGroup.addWidget(e1)
    
        # Color input
        gr1 = QHBoxLayout()
        gr2 = QHBoxLayout()
        self.GetColorButton = QPushButton("Выбрать цвет линии")
        self.GetBackColorButton = QPushButton("Выбрать цвет фона")
        self.GetColorButton.clicked.connect(self.get_color)
        self.GetBackColorButton.clicked.connect(self.get_back_color)
        
        self.ex_c1 = QWidget()
        self.ex_c2 = QWidget()
        self.ex_c1.setPalette(QPalette(self.color))
        self.ex_c1.setAutoFillBackground(True)
        
        self.ex_c2.setPalette(QPalette(self.back_color))
        self.ex_c2.setAutoFillBackground(True)
        
        gr1.addWidget(self.GetColorButton)
        gr1.addWidget(self.ex_c1)
        gr2.addWidget(self.GetBackColorButton)
        gr2.addWidget(self.ex_c2)
        
        # Combobox
        combo = QComboBox()
        combo.addItems(["Средней точки", "Брезенхема",
                        "Каноническое","Параметрическое",
                        "Стандартный"])
        combo.activated[str].connect(self.onActivated)
        
        self.FirstPage = QWidget()
        self.initFirstPageUI()

        self.SecondPage = QWidget()
        self.initSecondPageUI()
        
        self.tab = QTabWidget()
        self.tab.addTab(self.FirstPage,"Эллипс")
        self.tab.addTab(self.SecondPage,"Окружность")

        BGroup = QHBoxLayout()
        lbl_11 = QLabel("Шаг:")
        e11 = QLineEdit()
        e11.setValidator(QIntValidator(1,99999))
        e11.setAlignment(Qt.AlignRight)
        e11.setText("1")
        e11.setFont(QFont("Arial",12))
        e11.textChanged.connect(self.textchanged51)
        
        BGroup.addWidget(lbl_11)
        BGroup.addWidget(e11)
        
        # Packing into Group1
        Group1.addWidget(self.tab)
        Group1.addLayout(AGroup)
        Group1.addLayout(BGroup)
        Group1.addLayout(gr1)
        Group1.addLayout(gr2)
        Group1.addWidget(checkbox)
        Group1.addWidget(checkbox1)
        Group1.addWidget(combo)
        Group1.addLayout(h1)
        

    def initFirstPageUI(self):
        # (X1;Y1) Widgets
        AGroup = QHBoxLayout()
        lbl_11 = QLabel("Xc:")
        e11 = QLineEdit()
        e11.setValidator(QIntValidator())
        e11.setAlignment(Qt.AlignRight)
        e11.setText("250")
        e11.setFont(QFont("Arial",12))
        e11.textChanged.connect(self.textchanged11)
        
        AGroup.addWidget(lbl_11)
        AGroup.addWidget(e11)

        lbl_12 = QLabel("Yc:")
        e12 = QLineEdit()
        e12.setValidator(QIntValidator())
        e12.setAlignment(Qt.AlignRight)
        e12.setText("250")
        e12.setFont(QFont("Arial",12))
        e12.textChanged.connect(self.textchanged12)
        
        AGroup.addWidget(lbl_12)
        AGroup.addWidget(e12)

        # (X2;Y2) Widgets
        BGroup = QHBoxLayout()
        lbl_13 = QLabel("a:")
        e13 = QLineEdit()
        e13.setValidator(QIntValidator())
        e13.setAlignment(Qt.AlignRight)
        e13.setFont(QFont("Arial",12))
        e13.textChanged.connect(self.textchanged13)
        e13.setText("50")
        
        BGroup.addWidget(lbl_13)
        BGroup.addWidget(e13)

        lbl_14 = QLabel("b:")
        e14 = QLineEdit()
        e14.setValidator(QIntValidator())
        e14.setAlignment(Qt.AlignRight)
        e14.setFont(QFont("Arial",12))
        e14.textChanged.connect(self.textchanged14)
        e14.setText("20")
        
        BGroup.addWidget(lbl_14)
        BGroup.addWidget(e14)
        
        FirstPageL = QVBoxLayout()
        self.FirstPage.setLayout(FirstPageL)
        
        FirstPageL.addLayout(AGroup)
        FirstPageL.addLayout(BGroup)
        FirstPageL.addStretch()

        lbl_151 = QLabel("Конечное а для\nконцентрических эллипсов:")
        
        CGroup = QHBoxLayout()
        lbl_15 = QLabel("a_end:")
        e15 = QLineEdit()
        e15.setValidator(QIntValidator())
        e15.setAlignment(Qt.AlignRight)
        e15.setFont(QFont("Arial",12))
        e15.textChanged.connect(self.textchanged15)
        e15.setText(str(self.a))
        
        CGroup.addWidget(lbl_15)
        CGroup.addWidget(e15)

        FirstPageL.addWidget(lbl_151)
        lbl_152 = QLabel("Шаг задается ниже.")
        FirstPageL.addLayout(CGroup)
        FirstPageL.addWidget(lbl_152)
        FirstPageL.addStretch()

    
    def initSecondPageUI(self):
        # Angle
        AGroup = QFormLayout()
        e21 = QLineEdit()
        e21.setValidator(QIntValidator(1,999999))
        e21.setAlignment(Qt.AlignRight)
        e21.setFont(QFont("Arial",12))
        e21.textChanged.connect(self.textchanged21)
        e21.setText("250")

        e22 = QLineEdit()
        e22.setValidator(QIntValidator(0,999999))
        e22.setAlignment(Qt.AlignRight)
        e22.setFont(QFont("Arial",12))
        e22.textChanged.connect(self.textchanged22)
        e22.setText("250")
        
        e23 = QLineEdit()
        e23.setValidator(QIntValidator())
        e23.setAlignment(Qt.AlignRight)
        e23.setFont(QFont("Arial",12))
        e23.textChanged.connect(self.textchanged23)
        e23.setText("50")
        
        AGroup.addRow("Xc:",e21)
        AGroup.addRow("Yc:",e22)
        AGroup.addRow(" R:",e23)
        
        SecondPageL = QVBoxLayout()
        self.SecondPage.setLayout(SecondPageL)
        
        SecondPageL.addLayout(AGroup)
        lbl_241 = QLabel("Конечный радиус для\nконцентрических\nокружностей:")
        CGroup = QHBoxLayout()
        lbl_24 = QLabel("R_end:")
        e24 = QLineEdit()
        e24.setValidator(QIntValidator())
        e24.setAlignment(Qt.AlignRight)
        e24.setFont(QFont("Arial",12))
        e24.textChanged.connect(self.textchanged24)
        e24.setText(str(self.R))
        
        CGroup.addWidget(lbl_24)
        CGroup.addWidget(e24)
        SecondPageL.addStretch()
        
        SecondPageL.addWidget(lbl_241)
        lbl_152 = QLabel("Шаг задается ниже.")
        SecondPageL.addLayout(CGroup)
        SecondPageL.addWidget(lbl_152)
        SecondPageL.addStretch()


    def get_color(self):
        tmp = QColorDialog.getColor()

        if tmp.isValid():
            self.color = tmp
            self.ex_c1.setPalette(QPalette(self.color))
            self.ex_c1.setAutoFillBackground(True)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setText("Неверный цвет!")
            msg.setWindowTitle("Внимание!")
            msg.exec_()
        

    def get_back_color(self):
        tmp = QColorDialog.getColor()

        if tmp.isValid():
            self.back_color = tmp
            self.ex_c2.setPalette(QPalette(self.back_color))
            self.ex_c2.setAutoFillBackground(True)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setText("Вы не выбрали новый цвет!")
            msg.setWindowTitle("Внимание!")
            msg.exec_()


    def textchanged11(self, text):
        try:
            self.xc1 = int(text)
            self.flag[0][0] = True
        except:
            self.flag[0][0] = False


    def textchanged12(self, text):
        try:
            self.yc1 = int(text)
            self.flag[0][1] = True
        except:
            self.flag[0][1] = False


    def textchanged13(self, text):
        try:
            self.a = int(text)
            self.flag[0][2] = True
        except:
            self.flag[0][2] = False


    def textchanged14(self, text):
        try:
            self.b = int(text)
            self.flag[0][3] = True
        except:
            self.flag[0][3] = False


    def textchanged15(self, text):
        try:
            self.da = int(text)
            self.flag[0][4] = True
        except:
            self.flag[0][4] = False
    

    def textchanged21(self, text):
        try:
            self.xc2 = int(text)
            self.flag[1][0] = True
        except:
            self.flag[1][0] = False


    def textchanged22(self, text):
        try:
            self.yc2 = int(text)
            self.flag[1][1] = True
        except:
            self.flag[1][1] = False


    def textchanged23(self, text):
        try:
            self.R = int(text)
            self.flag[1][2] = True
        except:
            self.flag[1][2] = False  


    def textchanged24(self, text):
        try:
            self.dr = int(text)
            self.flag[1][3] = True
        except:
            self.flag[1][3] = False 


    def textchanged50(self, text):
        try:
            self.size = int(text)
            if self.size <= 0 or self.step <= 0:
                self.flag[2] = False
            else:
                self.flag[2] = True
        except:
            self.flag[2] = False


    def textchanged51(self, text):
        try:
            self.step = int(text)
            if self.step <= 0 or self.size <= 0:
                self.flag[2] = False
            else:
                self.flag[2] = True
        except:
            self.flag[2] = False 


    def onActivated(self, text):
        if text == "Средней точки":
            self.type = 0
        if text == "Брезенхема":
            self.type = 1
        if text == "Каноническое":
            self.type = 2
        if text == "Параметрическое":
            self.type = 3
        if text == "Стандартный":
            self.type = 4


    def changeColorToBack(self, state):
        if state == Qt.Checked:
            self.draw_back = True
        else:
            self.draw_back = False


    def chooseDrawType(self, state):
        if state == Qt.Checked:
            self.draw_type = 2
        else:
            self.draw_type = 3


    def add_ellipse(self):
        if not self.flag[2]:
            self.showdialog(1)
            return

        if self.draw_back:
            color = self.back_color
        else:
            color = self.color

        # Spectr
        if self.draw_type != 2 and self.draw_type != 3:
            # Ind 0(ellipse)
            if self.tab.currentIndex() == 0:
                for i in self.flag[0]:
                    if not i:
                        self.showdialog()
                        return

                self.draw_type = 0
                ellipse = [self.xc1, self.yc1,
                        self.a, self.b,
                        color, self.size,
                        self.type]
                self.ellipses.append(ellipse)
            # Ind 1(circle)
            elif self.tab.currentIndex() == 1:
                for i in self.flag[1]:
                    if not i:
                        self.showdialog()
                        return

                self.draw_type = 1
                circle = [self.xc2, self.yc2,
                        self.R, color, self.size,
                        self.type]
                self.circles.append(circle)
        # Single
        else:
            # Ind 0(ellipse)
            if self.tab.currentIndex() == 0:
                for i in self.flag[0]:
                    if not i:
                        self.showdialog()
                        return

                self.draw_type = 2

                a = self.a
                b = self.b
                step_b = round(self.step*(self.b/self.a))
                while a < self.da + self.step/2:
                    ellipse = [self.xc1, self.yc1,
                        a, b,
                        color, self.size,
                        self.type]
                    a += self.step
                    b += step_b
                
                    self.ellipses.append(ellipse)
            # Ind 1(circle)
            elif self.tab.currentIndex() == 1:
                for i in self.flag[1]:
                    if not i:
                        self.showdialog()
                        return
                
                self.draw_type = 3

                r = self.R
                while r < self.dr + self.step/2:
                    circle = [self.xc2, self.yc2,
                        r, color, self.size,
                        self.type]
                    r += self.step
                
                    self.circles.append(circle)

        self.Canv.type = self.draw_type % 2


    def showdialog(self,flag=0):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        if flag != 1:
            text = ("Какие-то из полей пустые или запонены неправильно!"+
                    "\nНевозможно выполнить операцию!")
        else:
            text = ("Размер или шаг заданы неверно или не заданы!"+"\nОни должны быть положительные!"+
                    "\nНевозможно выполнить операцию!")
        msg.setText(text)
        msg.setWindowTitle("Внимание!")
        msg.exec_()

    
    def clear(self):
        self.circles = []
        self.ellipses = []
        self.endFlag = 0
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


