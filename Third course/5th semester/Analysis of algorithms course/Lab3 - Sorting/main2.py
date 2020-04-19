from sort import *
from main1 import get_calc_time

arr = list(map(int,input().split(' ')))
arr1 = arr.copy()
arr2 = arr.copy()
arr3 = arr.copy()

print("\nСортировка пузырьком:")
print(get_calc_time(mysort_bubble, arr1))
#print(arr1)


print("\nСортировка вставками:")
print(get_calc_time(mysort_insert, arr2))
#print(arr2)

print("\nБыстрая сортировка:")
print(get_calc_time(mysort_quick_end, arr3))
#print(arr3)
