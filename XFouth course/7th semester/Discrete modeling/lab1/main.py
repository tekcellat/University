from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
import scipy.stats as stats
import random
from itertools import islice

class MersenneTwister:
    mask = int('0bFFFFFFFF', 16)  # маска для 32-битного числа
    mask32th = int('0b990B0DF', 16)  # маска для старшего бита
    mask31th = int('0b7FFFFFFF', 16)  # маска для оставшихся 31 битов
    index = 0
    n = 624  # количество плоскостей
    magic = 623  # магическая константа для генерации
    # 32-битные константы
    A = int('0b9908B000DF', 16)
    B = int('0b9D2C568016', 16)
    C = int('0bEFC6000016', 16)

    m = 397  # сдвиг
    r = 31
    l = 18
    u = 11
    s = 7
    t = 15

    MT = []

    # заполнение вектора
    def __init__(self):
        self.MT = [0] * self.n
        seed = self.mask & random.randint(0, sys.maxsize)
        self.MT[0] = seed

        for i in range(1, self.n):
            self.MT[i] = (self.magic * (self.MT[i - 1] ^ (self.MT[i - 1] >> 30))) + i
        self.__twister__()

    # закалка вектора
    def __twister__(self):
        for i in range(self.n):
            tmp = ((self.MT[i] & self.mask32th) + (self.MT[(i + 1) % self.n]) & self.mask31th)
            self.MT[i] = (self.MT[(i + 1) % self.n] ^ (tmp >> 1)) & self.mask
            if tmp % 2 == 1:
                self.MT[i] = self.MT[i] ^ self.A

    def get_number(self):
        if self.index == 0:
            self.__init__()

        x = self.MT[self.index]
        x = x ^ (x >> self.u)
        x = x ^ (x << self.s) & self.B
        x = x ^ (x << self.t) & self.C
        x = x ^ (x << self.l)

        self.index = (self.index + 1) % self.n

        return x

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.fill.clicked.connect(lambda: on_fill_click(self))
        self.manual_input.returnPressed.connect(lambda: on_manual_input_enter(self))
        self.meas_alg_1.setReadOnly(True)
        self.meas_alg_2.setReadOnly(True)
        self.meas_alg_3.setReadOnly(True)
        self.meas_table_1.setReadOnly(True)
        self.meas_table_2.setReadOnly(True)
        self.meas_table_3.setReadOnly(True)
        self.meas_manual.setReadOnly(True)
        self.alg_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.line_num = 0

        for i in range(10):
            self.alg_table.insertRow(i)

        for i in range(10):
            self.table_table.insertRow(i)


#здесь считается критерий
def k_stat(arr):
    n = len(arr) - 1
    h = 0
    l = 0

    for i in range(1, len(arr)):
        if (arr[i] - arr[i - 1]) > 0:
            h += 1
        else:
            l += 1

    h /= n
    l /= n

    return abs(h - l)

#здесь получается массив
def get_number(Twister, par):

    arr = []
    for i in range(1000):
        arr.append( int((par / 10)) + Twister.get_number() % par)

    return arr

def on_fill_click(win):

    #здесь генерируются числа
    table = win.alg_table

    mt = MersenneTwister()
    one_digit = get_number(mt, 10)
    two_digits = get_number(mt, 100)
    three_digits = get_number(mt, 1000)


    for i in range(10):
        item = QTableWidgetItem(str(one_digit[i]))
        table.setItem(i, 0, item)

    for i in range(10):
        item = QTableWidgetItem(str(two_digits[i]))
        table.setItem(i, 1, item)

    for i in range(10):
        item = QTableWidgetItem(str(three_digits[i]))
        table.setItem(i, 2, item)

    entropy_one = k_stat(one_digit)
    entropy_two = k_stat(two_digits)
    entropy_three = k_stat(three_digits)
    win.meas_alg_1.setText('{:.4%}'.format(entropy_one))
    win.meas_alg_2.setText('{:.4%}'.format(entropy_two))
    win.meas_alg_3.setText('{:.4%}'.format(entropy_three))


    #здесь числа берутся из файла
    table = win.table_table
    numbers = set()
    with open('digits.txt') as file:
        lines = islice(file, win.line_num, None)
        for l in lines:
            numbers.update(set(l.split(" ")[1:-1]))
            win.line_num += 1
            if len(numbers) >= 3001:
                break
        numbers.remove("")
        numbers = list(numbers)[:3000]


    one_digit = [int(i) % 9 + 1 for i in numbers[:1000]]
    two_digits = [int(i) % 90 + 10 for i in numbers[1000:2000]]
    three_digits = [int(i) % 900 + 100 for i in numbers[2000:3000]]

    for i in range(10):
        item = QTableWidgetItem(str(one_digit[i]))
        table.setItem(i, 0, item)

    for i in range(10):
        item = QTableWidgetItem(str(two_digits[i]))
        table.setItem(i, 1, item)

    for i in range(10):
        item = QTableWidgetItem(str(three_digits[i]))
        table.setItem(i, 2, item)

    entropy_one = k_stat(one_digit)
    entropy_two = k_stat(two_digits)
    entropy_three = k_stat(three_digits)
    win.meas_table_1.setText(' {:.4%}'.format(entropy_one))
    win.meas_table_2.setText(' {:.4%}'.format(entropy_two))
    win.meas_table_3.setText(' {:.4%}'.format(entropy_three))


def on_manual_input_enter(win):
    input = win.manual_input
    measure = win.meas_manual
    sequence = input.text().split(" ")
    filtered_sequence = []
    for i in sequence:
        try:
            int(i)
        except ValueError:
            continue
        else:
            filtered_sequence.append(i)

    entropy = k_stat(list(map(lambda x: int(x), filtered_sequence)))
    win.meas_manual.setText(' {:.4%}'.format(entropy))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())