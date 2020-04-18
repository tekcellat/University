/* Принимает из аргументов командной строки имя файла с массивом целых чисел,
 * находит max(a[0] + a[n - 1], a[1] + a[n - 2], ...). Если количество чисел
 * нечетное, то рассматривается также число a[(n - 1) / 2] */

#include <stdio.h>

#define NMAX 100
#define SUCCESS 0
#define WRONG_PARAMETERS -1
#define FILE_ERROR -2
#define EMPTY_FILE -3
#define INPUT_ERROR -4

/* Проверяет содержимое файла f с целыми числами типа int на корректность,
 * записывает эти числа в массив a и устанавливает указатель pend на
 * последний элемент массива */
int read_array(FILE *f, int *a, int *const n)
{
    int temp;

    *n = 0;

    // Считывание чисел
    while (fscanf(f, "%d", &temp) == 1 && (*n)++ < NMAX)
        *(a++) = temp;

    // Обработка исключительных ситуаций
    if (*n == NMAX + 1)
    {
        printf("Length exceeds %d\n", NMAX);
        (*n)--;
    }
    else if (feof(f) == 0)
    {
        fprintf(stderr, "Input error");

        return INPUT_ERROR;
    }
    else if (*n == 0)
    {
        fprintf(stderr, "Empty file");

        return EMPTY_FILE;
    }

    return SUCCESS;
}

/* Находит max(a[0] + a[n - 1], a[1] + a[n - 2], ...) целочисленного массива
 * с указателем на начальный элемент p1 и на последний элемент p2 */
int count(const int *pbegin, const int *pend, int *const max)
{
    if (pbegin >= pend)
        return WRONG_PARAMETERS;

    // Присваиваем *max начальное значение
    if (pbegin != pend)
        *max = *pbegin + *pend;
    else
        *max = *pbegin;

    // Основной цикл
    for (; pbegin < pend; pbegin++, pend--)
        if (*pbegin + *pend > *max)
            *max = *pbegin + *pend;

    // Если осталось одно число в середине массива
    if (pbegin == pend && *max < *pend)
        *max = *pend;

    return SUCCESS;
}

int main(int argc, char **argv)
{
    FILE *f;
    int a[NMAX], *pend, n = 0; //pend - указатель на последний элемент массива a
    int max;
    int status;

    //Проверка количества параметров командной строки
    if (argc != 2)
    {
        fprintf(stderr, "Wrong parameters\nmain.exe <file-name>\n");

        return WRONG_PARAMETERS;
    }

    //Проверка и открытие файла
    f = fopen(argv[1], "r");
    if (f == NULL)
    {
        perror("Error opening file");

        return FILE_ERROR;
    }

    status = read_array(f, a, &n);

    pend = a + n - 1;

    if (status == SUCCESS) //нахождение и вывод искомой величины
    {
        count(a, pend, &max);
        printf("%d", max);
    }

    // Закрытие файла
    if (fclose(f) != 0)
    {
        perror("Error closing file");

        return FILE_ERROR;
    }

    return status;
}
