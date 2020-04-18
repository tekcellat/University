// Выводит среднее арифметическое отрицательных элементов вводимого массива

#include <stdio.h>

#define SUCCESS 0
#define WRONGNUMBER -1
#define WRONGLENGTH -2
#define NONEGATIVENUMBERS -3
#define NMAX 10

/* Принимает указатель на первый элемент массива и указатель на размер массива,
 * считывает с консоли не более Nmax числел типа int в массив */
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

/* Принимает указатель на первый элемент целочисленного массива, размер
 * массива и указатель на вычисляемую переменную среднего арифметического
 * отрицательных чисел массива */
int count_neg_average(const int *const a, const int n, float *const average)
{
    int n_neg = 0, sum_neg = 0;

    for (int i = 0; i < n; i++)
        if (a[i] < 0)
        {
            sum_neg += a[i];
            n_neg++;
        }

    if (n_neg == 0)
        return NONEGATIVENUMBERS;

    *average = (float) sum_neg / n_neg;

    return SUCCESS;
}

int main(void)
{
    int a[NMAX], n = 0;
    float average;
    int status;

    printf("Write array and press ENTER:\n");

    // Считываем массив
    status = read_array(a, &n);
    if (status != SUCCESS)
        return status;

    status = count_neg_average(a, n, &average);

    // Вывод результата
    if (status == NONEGATIVENUMBERS)
        fprintf(stderr, "No negative numbers");
    else printf("%f", average);

    return status;
}
