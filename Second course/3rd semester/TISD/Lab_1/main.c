/**
 * \file main.c
 * \brief Главный файл. Умножение. Вариант 5
 */
 
#include <stdio.h>
#include "read_number.h"
#include "multiply.h"
#include "print_number.h"

int main(void)
{   
    char sign, sign1, sign2;
    short int num1[30], na1, nb1; // Цифры первого числа, кол-во знаков до и после точки
    short int num2[30], na2, nb2; // Цифры второго числа, кол-во знаков до и после точки
    int exp1, exp2; // Порядок первого и второго числа
    short int result[60] = {0};

    // Выводим информацию
    printf("Multiplication\n");
    printf("Print numbers in format: (+/-)m.n E k\nWhere m + n are less than ");
    printf("31 digits\nk is less than 6 digits\n---\nFor example: -31.6 E -3\n");
    printf("The first:                      |\n");
    
    // Вводим первое число
    if (read_number(&sign1, num1, &na1, &nb1, &exp1) != SUCCESS)
    {
        printf("Error, wrong input");
        
        scanf("%c%c", &sign1, &sign2);
        return WRONG_INPUT;
    }
    
    // Вводим второе число
    printf("The second:                     |\n");
    if (read_number(&sign2, num2, &na2, &nb2, &exp2) != SUCCESS)
    {
        printf("Error, wrong input");
        
        scanf("%c%c", &sign1, &sign2);
        return WRONG_INPUT;
    }
    
    // Убираем точку в числах за счет уменьшения порядка
    exp1 -= nb1;
    exp2 -= nb2;
    
    // Выбираем нужный знак
    if (sign1 == sign2)
        sign = '+';
    else 
        sign = '-';
    
    // Умножаем числа
    multiply(num1, num2, na1 + nb1, na2 + nb2, result);
    
    // Выводим на экран
    if (print_number(sign, result, exp1 + exp2) != SUCCESS)
    {
        printf("Error, overflow");
        
        scanf("%c", &sign1);
        return OVERFLOW;
    }    
    
    scanf("%c", &sign1);
    return SUCCESS;
}