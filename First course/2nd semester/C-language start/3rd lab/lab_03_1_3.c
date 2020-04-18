/* Определяет, сколько раз во вводимой последовательности
 * целых чисел меняется знак */

#include <stdio.h>

#define SUCCESS 0
#define NO_DATA -1

// Записывает в result количество чередований знаков целых чисел из файла f
int process(FILE *f, int *const result)
{
    int num1, num2;
    char c;

    *result = 0;
    rewind(f);

    printf("Numbers: ");

    //Считывание первого числа
    if (fscanf(f, "%d%c", &num1, &c) != 2)
        return NO_DATA; //нет ни одного числа
    else if (c != ' ')
        return SUCCESS;

    // Подсчет чередований знаков
    while (fscanf(f, "%d%c", &num2, &c) == 2)
    {
        if ((num1 < 0 && num2 >= 0) || (num1 >= 0 && num2 < 0))
            (*result)++;

        if (c != ' ')
            return SUCCESS;

        num1 = num2;
    }

    return SUCCESS;
}

int main(void)
{
    int status;
    int result; //количество чередований

    status = process(stdin, &result);

    if (status == SUCCESS)
        printf("%d", result);
    else
        fprintf(stderr, "No input data");

    return status;
}
