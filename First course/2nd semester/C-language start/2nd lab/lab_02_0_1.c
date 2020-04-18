//Возведение числа в степень

#include <stdio.h>

#define SUCCESS 0

#define UNSUCCESS 1

//Возводит число a в степень n
int power(int a, int n)
{
    int result = 1;

    for (; n > 0; n--) //цикл возведения в степень
        result *= a;

    return result;
}

// Считывает два числа типа int, второе - неотрицательное
int read_2_numbers(int *const pa, int *const pn)
{
    if (scanf("%d %u", pa, pn) != 2 || *pn < 0)
    {
        printf("Input error");
        return UNSUCCESS;
    }
    else
        return SUCCESS;
}

int main(void)
{
    int a, n;

    //Считываем данные
    printf("Write a and n: ");

    if (read_2_numbers(&a, &n) == UNSUCCESS)
            return UNSUCCESS;

    if (a == 0 && n == 0) //0^0 - математическая неопределенность
        printf("Not defined");
    else
        printf("%d", power(a, n)); //выводим результат

    return SUCCESS;
}
