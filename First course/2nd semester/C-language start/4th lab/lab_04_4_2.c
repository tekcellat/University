// Сортирует вводимый массив по возрастанию выбором

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

// Возвращает индекс мин. элемента массива a длиной n начиная с индекса i
int find_min(const int *const a, const int i, const int n, int *const imin)
{
    if (i >= n)
        return WRONGPARAMETERS;

    *imin = i;

    // Нахождение минимального элемента на интервале
    for (int j = i + 1; j < n; j++)
        if (a[j] < a[*imin])
            *imin = j;

    return SUCCESS;
}

/* Принимает указатель на первый элемент целочисленного массива и
 * размер массива, сортирует массив по возрастанию выбором,
 * возвращает количество переставленных элементов */
int sort_array(int *const a, const int n)
{
    int n_per = 0;

    for (int i = 0, imin, min; i < n - 1; i++)
    {
        find_min(a, i, n, &imin);

        // Перемещение минимального элемента на i-ое место
        if (a[imin] != a[i])
        {
        min = a[imin];
        a[imin] = a[i];
        a[i] = min;
        n_per++;
        }
    }

    return n_per;
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

    // Считывает массив
    status = read_array(a, &n);

    if (status == SUCCESS) //сортирует и выводит на экран массив
    {
        sort_array(a, n);
        print_array(a, n);
    }

    return status;
}
