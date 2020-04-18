/* Выводит элементы вводимого массива, которые начинаются и заканчиваются
 * на одну и ту же цифру */

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
 * на размер массива, оставляет в массиве числа, начинающиеся
 * и заканчивающиеся на одну и ту же цифру, возвращает количество удаленных
 * элементов */
int change_array(int *const a, int *const n)
{
    int n0 = *n; //количество элементов данного массива

    for (int i = 0, first_digit, last_digit; i < *n; i++)
    {
        last_digit = abs(a[i] % 10);
        first_digit = abs(a[i]);

        while (first_digit > 9)
            first_digit /= 10;

        if (last_digit != first_digit)
            delete_number(a, n, i--);
    }

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
    int a[NMAX], n = 0;
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
        printf("No numbers");

    return status;
}
