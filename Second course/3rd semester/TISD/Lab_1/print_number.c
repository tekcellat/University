/**
 * \file print_number.c
 * \brief Функция print_number()
 */
 
#include <stdio.h>
#include "print_number.h"

/**
 * \fn int print_number(const char sign, int *result, int exp)
 * \brief Приводит число к стандартной форме и выводит на экран
 * \param [in] sign Знак результата (+/-)
 * \param [in] result Указатель на массив цифр результата
 * \param [in] exp Показатель числа
 * \return Код выполнения
 */
int print_number(const char sign, short int *result, int exp)
{
    short int nresult; // Количество цифр результата
    int i = 0;
    
    // Убираем нули слева от результата
    while (i < 60 && result[i] == 0)
    {
        i++;
    }
    
    nresult = 60 - i;
    result += i;
    
    //Вычисляем и проверяем на переполнение итоговый порядок
    exp += nresult;
    
    if (exp > 99999 || exp < -99999)
        return OVERFLOW;
    
    // Округляем до 30 значащих цифр
    if (nresult > 30)
    {
        nresult = 30;
        
        if (result[30] >= 5)
        {
            result[29] += 1;
            
            for (int i = 29; result[i] == 10; i--)
            {
                result[i] = 0;
                result[i-1] += 1;
            }
        }
    }
    
    // Убираем нули справа
    for (int i = nresult - 1; i >= 0; i--)
        if (result[i] == 0)
            nresult--;
        else
            break;
    
    // Если рузельтат - 0
    if (nresult == 0)
        printf("\nResult: 0");
    // Иначе выводим в стандартной форме
    else
    {
        printf("\nResult: %c0.", sign);
        
        for (int i = 0; i < nresult; i++)
            printf("%d", result[i]);
        
        if (exp != 0)
            printf(" E %d", exp);
    }
    
    return SUCCESS;
}