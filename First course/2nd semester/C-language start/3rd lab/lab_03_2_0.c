/* Находит среди вводимых вещественных чисел типа float число,
 * наиболее близкое к среднему значению всех чисел */

#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>

#define SUCCESS 0
#define WRONG_PARAMETERS -1
#define FILE_ERROR -2
#define EMPTY_FILE -3
#define INPUT_ERROR -4

/* Проверяет содержимое файла f с целыми числами типа int на корректность и
 * записывает среднее арифметическое этих чисел в av */
int count_average(FILE *f, float *const av)
{    
    float sum, temp = 0;
    int num = 0;

    rewind(f);

    // Считывание чисел
    while (fscanf(f, "%f", &temp) == 1)
    {
        sum += temp;
        num++;
    }

    // Обработка ошибок
    if (feof(f) == 0)
    {
        fprintf(stderr, "Input error");

        return INPUT_ERROR;
    }
    else if (num == 0)
    {
        fprintf(stderr, "Empty file");

        return EMPTY_FILE;
    }

    *av = sum / num;

    return SUCCESS;
}

/* Записывает наиболее близкие к av числа типа float из файла f в num1 и num2
 * Проверка на корректность не выполняется */
int define_nearest(FILE *f, const float *const av, float *const num1,
                                                   float *const num2)
{
    float temp;

    rewind(f);

    // Считывание первого числа
    if (fscanf(f, "%f", num1) != 1)
        return FILE_ERROR;

    *num2 = *num1;

    //Считывание и проверка всех чисел
    while (fscanf(f, "%f", &temp) == 1)
    {
        if (fabs(2 * (*av) - *num1 - temp) < 10e-7)
            *num2 = temp;
        else if (fabs(*av - temp) - fabs(*av - *num1) < 10e-7)
            *num1 = *num2 = temp;
    }

    return SUCCESS;
}

int main(int argc, char **argv)
{
    FILE *f;
    float av; //среднее арифметическое чисел
    int status;
    float num1, num2; //искомые числа

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
        fprintf(stderr, "File error: %s", argv[1]);

        return FILE_ERROR;
    }

    status = count_average(f, &av);

    // Находим искомые числа
    if (status == SUCCESS)
    {
        if (define_nearest(f, &av, &num1, &num2) == SUCCESS)
        {
            printf("%f", num1);
            if (num1 != num2) //если есть второе число
                printf(" %f", num2);
        }
        else
            status = FILE_ERROR;
    }

    if (fclose(f) != 0)
    {
        fprintf(stderr, "Error closing file: %s", strerror(errno));
        return FILE_ERROR;
    }

    return status;
}
