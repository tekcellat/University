

def calc_n_plus_1_ksi(ksi_n, C_n, B_n, A_n):
    return C_n / (B_n - A_n * ksi_n)

def calc_n_plus_1_etta(ksi_n, etta_n, B_n, A_n, F_n):
    return (F_n + A_n * etta_n) / (B_n - A_n * ksi_n)


def calc_y_n(ksi_n_plus_1, etta_plus_1, y_plus_1):
    return ksi_n_plus_1 * y_plus_1 + etta_plus_1

def progonka(A_n, B_n, C_n, F_n, K_0, M_0, P_0, K_N, M_N, P_N):

    ksi = []
    etta = []
    y_result = []

    #начальные кси и этта
    ksi_1 = -M_0 / K_0
    etta_1 = P_0 / K_0

    ksi.append(ksi_1)
    etta.append(etta_1)

    #вычисление всех кси и этта
    for i in range(len(A_n)):
        ksi.append(calc_n_plus_1_ksi(ksi[i], C_n[i], B_n[i], A_n[i]))
        etta.append(calc_n_plus_1_etta(ksi[i], etta[i], B_n[i], A_n[i], F_n[i]))


    #вычисление y_N
    y_N = (P_N - M_N * etta[i]) / (K_N + M_N * ksi[i])

    y_result.append(y_N)

    #вычислене всех y_n
    for i in range(len(ksi) - 1, -1, -1):
        y_result.append(calc_y_n(ksi[i], etta[i], y_result[-1]))

    y_result.reverse()

    return y_result