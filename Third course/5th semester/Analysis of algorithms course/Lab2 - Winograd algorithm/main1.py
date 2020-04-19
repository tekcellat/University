from func import *

def measure_time(n1, n2, st, it):
    t_ord_matr_mul = []
    t_vin_matr_mul = []
    t_opt_vin_matr_mul = []
    for n in range(n1, n2, st):
        print(n, ' ', time.time())
        a = get_random_matrix(n)
        b = get_random_matrix(n)
        c =  get_zero_matrix(len(a))
        t_ord_matr_mul.append(get_calc_time(ord_matr_mul, a, b, c, it))

        c = get_zero_matrix(len(a))
        t_vin_matr_mul.append(get_calc_time(vin_matr_mul, a, b, c, it))

        c = get_zero_matrix(len(a))
        t_opt_vin_matr_mul.append(get_calc_time(opt_vin_matr_mul, a, b, c, it))

    return (t_ord_matr_mul, t_vin_matr_mul, t_opt_vin_matr_mul)

n1 = int(input("Size\nFrom: "))
n2 = int(input("To: "))
h = int(input("Step: "))
#againts any problem
if n1 > n2 or n2 == n1 or h == 0:
    print("Wrong input")
    exit()
else:
    result = measure_time(n1, n2 + 1, h, 5)
    print(result)
