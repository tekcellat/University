from func import *

matr1 = input_matrix("A:")
matr2 = input_matrix("\nB:")
matr3 = get_zero_matrix(len(matr1), len(matr2[0]))
if len(matr1) == len(matr2):
    print("\nСтандартный алгоритм умножения матриц:")
    print_matrix(ord_matr_mul(matr1, matr2, matr3))

    matr3 = get_zero_matrix(len(matr1), len(matr2[0]))
          
    print("\nАлгоритм Винограда:")
    print_matrix(vin_matr_mul(matr1, matr2, matr3))

    matr3 = get_zero_matrix(len(matr1), len(matr2[0]))

    print("\nАлгоритм Винограда с набором оптимизаций:")
    print_matrix(opt_vin_matr_mul(matr1, matr2, matr3))
else:
    print('Error! Whong size')
