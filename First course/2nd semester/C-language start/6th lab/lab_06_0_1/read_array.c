#include <stdio.h>

#define SUCCESS 0
#define EMPTY_FILE -3
#define INPUT_ERROR -4
#define NMAX 100

/* Проверяет содержимое файла f с целыми числами типа int на корректность,
 * записывает эти числа в массив a */
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
        printf("Input error");

        return INPUT_ERROR;
    }
    else if (*n == 0)
    {
        printf("Empty file");

        return EMPTY_FILE;
    }

    return SUCCESS;
}
