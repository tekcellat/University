/**
 * \file multiply.c
 * \brief Функция multiply()
 */
 
#include "multiply.h"

/**
 * \fn int multiply(const int *num1, const int *num2, const int n1,
   const int n2, int *const result)
 * \brief Умножает два больших числа
 * \param [in] num1 Указатель на массив цифр первого числа
 * \param [in] num2 Указатель на массив цифр второго числа
 * \param [in] n1 Длина первого числа
 * \param [in] n2 Длина второго числа
 * \param [out] result Указатель на массив цифр результата
 * \return Код выполнения
 */
int multiply(const short int *num1, const short int *num2, const short int n1,
   const short int n2, short int *const result)
{
    int temp[60]; // Промежуточная сумма умножнения
    
    // Обнуляем result
    for (int i = 0; i < 60; i++)
        result[i] = 0;
    
    // Умножаем
    for (int i = 0; i < n2; i++)
    {
        // Обнуляем temp
        for (int x = 0; x < 60; x++)
            temp[x] = 0;
        
        // Перемножаем разряды чисел
        for (int ost = 0, j = 0; j < n1; j++) // ost - перенос на следующий разряд
        {
            ost += (*(num2 + n2 - 1 - i))*(*(num1 + n1 - 1 - j));
            temp[59 - i - j] = ost % 10; 
            ost /= 10;
            
            if (j == n1 - 1)
                temp[58 - i - j] = ost;
        }
        
        // Прибавляем полученную промежуточную сумму к результату
        for (int ost = 0, x = 59; x >= 0; x--)
        {
            ost = ost + result[x]+ temp[x];
            result[x] = ost % 10;
            ost /= 10;
        }
    }
    
    return SUCCESS;
}