from sort import *
import time
import random

def get_random_array(n):
    array = []
    
    for i in range(n):
        array.append(random.randint(0, 20000))

    return array

def get_best_array(n):
    array = []
    
    for i in range(n):
        array.append(i)

    return array

def get_worst_array(n):
    array = []
    
    for i in range(n):
        array.append(n - i)

    return array

def get_calc_time(func, arr):
    t2 = time.process_time()
    func(arr)
    t1 = time.process_time() - t2

    return t1

def measure_time(get_array, get_array_quick, func, n1, n2, st, it):
    t_bubble = []
    t_shell = []
    t_quick = []
    
    for n in range(n1, n2, st):
        print(n, ' ', time.time())
        t = 0
        
        for i in range(it):
            arr = get_array(n)
            t += get_calc_time(mysort_bubble, arr)
        
        t_bubble.append(t / it)
        t = 0

        for i in range(it):
            arr = get_array(n)
            t += get_calc_time(mysort_insert, arr)
        
        t_shell.append(t / it)
        t = 0

        for i in range(it):
            arr = get_array_quick(n)
            t += get_calc_time(func, arr)
        
        t_quick.append(t / it)

    return (t_bubble, t_shell, t_quick)

n1 = int(input("Size\nFrom: "))
n2 = int(input("To: "))
h = int(input("Step:"))

if n1 > n2 or n2 == n1 or h == 0:
    print("Wrong input")
    exit()
    
else:
    result = measure_time(get_best_array, get_best_array, mysort_quick_middle, n1, n2 + 1, h, 100)
    print("\n", result, "\n")

    result = measure_time(get_worst_array, get_best_array, mysort_quick_end, n1, n2 + 1, h, 100)
    print("\n", result, "\n")

    result = measure_time(get_random_array, get_random_array, mysort_quick_middle, n1, n2 + 1, h, 100)
    print("\n", result, "\n")
