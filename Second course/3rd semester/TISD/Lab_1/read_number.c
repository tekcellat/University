/**
 * \file read_number.c
 * \brief Функция read_number()
 */
 
#include <stdio.h>
#include <ctype.h>
#include "read_number.h"

/**
 * \fn int read_number(char *const sign, int *const num, int *const na,
  int *const nb, int *const exp)
 * \brief Считывает число в нужном формате
 * \param [out] sign Указатель на знак числа(+/-)
 * \param [out] num Указатель на массив цифр числа
 * \param [out] na Указатель на количество цифр числа до точки
 * \param [out] nb Указатель на количество цифр числа после точки
 * \param [out] exp Указатель на показатель числа
 * \return Код выполнения
 */
int read_number(char *const sign, short int *const num, short int *const na,
  short int *const nb, int *const exp)
{
    int stage = 0; // Стадия ввода: 0 - знак, 1 - до точки, 2 - после точки
    char temp;
    
    *na = *nb = 0;
    *sign = '+';
    *exp = 0;
    
    scanf("%c", &temp);
    
    // Цикл считывания символов
    while (temp != '\n')
    {   
        // Если введен знак
        if (temp == '+' || temp == '-')
        {
            if (stage == 0)
            {
                stage = 1;
                *sign = temp;
            }
            else
                return WRONG_INPUT;
        }
        
        // Если введена цифра
        else if (isdigit(temp))
        {
            //  До запятой
            if (stage < 2 && (*na + *nb < 30)) 
            {
                stage = 1;
                num[(*na)++] = (int) temp - 48;
            }
            
            // После запятой
            else if ((*na + *nb) < 30) 
                num[*na + (*nb)++] = (int) temp - 48;
                
            else
                return WRONG_INPUT;
        }
        
        // Если введена точка 
        else if (temp == '.')
            if (stage == 2)
                return WRONG_INPUT;
            else
                stage = 2;  
            
        // Если введен пробел
        else if (temp == ' ')
        {           
            if (scanf("E %d", exp) != 1 || *exp > 99999 || *exp < -99999)
                return WRONG_INPUT;
        }
            
        // Если введен некорректный символ
        else
            return WRONG_INPUT;
        
        scanf("%c", &temp);
    }
    
    // Проверка, вводилось ли хоть что-то
    if (*na || *nb || *exp)
        return SUCCESS;
    else
        return WRONG_INPUT;
}
