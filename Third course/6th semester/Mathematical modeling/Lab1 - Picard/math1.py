from prettytable import PrettyTable
#addim
h = 0.0000001

#   aslinda cauchy problemidir:
#   u'(x) = func(x, u) = x^2 + u^2
#   u(0) = 0;y(0) = u(0)
def function(x,u): return pow(x,2)+pow(u,2)

def Picar3(x):
    y = pow(x, 3) / 3
    tmp = 1 + pow(x, 4) / 21
    tmp += 2 * pow(x, 3) / (693)
    tmp += pow(x, 12) / (19845)
    return y*tmp


def Picar4(x):
    y = pow(x, 31)/109876902975
    y += 2 * pow(x, 23) / 86266215
    y += 2 * pow(x, 22) / 1361505915
    y += 2 * pow(x, 19) / 3393495
    y += pow(x, 15) / 59535
    y += 2 * pow(x, 14) / 916839
    y += pow(x, 13) / 56189133
    y += 2 * pow(x, 11)/2079
    y += 2 * pow(x, 10)/31185
    y += 2 * pow(x, 7)/63
    y += pow(x, 3) / 3
    return y

#sayisal yontem (coklu cizgi yontemi)
def polyline(x, y): return (y + h * function(x, y))

def Runge2(x, y):
    return y + h * function(x + h / 2, y + h / 2 * function(x, y))

def Runge4(x, y):
    K1 = function(x, y)
    K2 = function(x + h / 2, y + h * K1 / 2)
    K3 = function(x + h / 2, y + h * K2 / 2)
    K4 = function(x + h, y + h * K3)
    return y + h / 6 * (K1 + 2 * K2 + 2 * K3 + K4)

def main():
    #sinirlar
    x = 0.0
    maxX = 2
    poly = 0.0
    run2 = 0.0
    run4 = 0.0
    tb = PrettyTable([" X ","Picard 3", "Picard 4", "Polyline явный", "Runge 2nd неявный", "Runge 4th"])
    
    while(x <= maxX):
        tb.add_row([round(x, 7), round(Picar3(x), 7), round(Picar4(x), 7), round(poly, 7), round(run2, 7), round(run4, 7)])
        poly = polyline(x, poly)
        run2 = Runge2(x, run2)
        run4 = Runge4(x, run4)
        x += h
    print(tb, "\n")
    return 0
main()




