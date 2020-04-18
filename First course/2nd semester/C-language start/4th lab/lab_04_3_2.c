/* Удаляет из вводимого массива все элементы, которые являются полными
 * квадратами, и выводит его на экран */

#include <stdio.h>
#include <math.h>

#define SUCCESS 0
#define WRONGNUMBER -1
#define WRONGLENGTH -2
#define WRONGPARAMETERS -3
#define NMAX 10

/* Принимает указатель на первый элемент массива и указатель на размер массива,
 * считывает с консоли не более Nmax чисел типа int в массив */
int read_array(int *const a, int *const n)
{
    int temp;
    char c;

    // Цикл считывания чисел
    while (scanf("%d%c", &temp, &c) == 2 && (*n)++ < NMAX && c == ' ')
        a[*n - 1] = temp;
    a[*n - 1] = temp;

    // Обработка ошибочных ситуаций
    if (*n > NMAX)
    {
        fprintf(stderr, "Length exceeds 10");

        return WRONGLENGTH;
    }
    else if (c != '\n')
    {
        fprintf(stderr, "Wrong number");

        return WRONGNUMBER;
    }

    return SUCCESS;
}

/* Принимает указатель на первый элемент целочисленного массива, указатель
 * на размер массива и индекс числа, удаляет из массива число
 * с соответствующим индексом */
int delete_number(int *const a, int *const n, const int num_index)
{
    if (*n <= num_index)
        return WRONGPARAMETERS;

    for (int i = num_index; i < *n - 1; i++)
        a[i] = a[i + 1];

    *n -= 1;

    return SUCCESS;
}

/* Принимает указатель на первый элемент целочисленного массива и указатель
 * на размер массива, оставляет в массиве числа, не являющиеся
 * полными квадратами, возвращает количество удаленных чисел */
int change_array(int *const a, int *const n)
{
    int n0 = *n;

    for (int i = 0; i < *n; i++)
        if (a[i] >= 0 && sqrt(a[i]) == (int) sqrt(a[i]))
            delete_number(a, n, i--);

    return n0 - *n;
}

/* Принимает указатель на первый элемент целочисленного массива и размер
 * массива, выводит массив на экран */
void print_array(const int *const a, const int n)
{
    for (int i = 0; i < n; i++)
        printf("%d ", a[i]);
    printf("\n");
}

int main(void)
{
    int a[NMAX], n;
    int status;

    printf("Write array and press ENTER:\n");

    // Считываем массив
    status = read_array(a, &n);
    if (status != SUCCESS)
        return status;

    change_array(a, &n);

    if (n > 0)
        print_array(a, n);
    else
        printf("No numbers left");

    return status;
}
