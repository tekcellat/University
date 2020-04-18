//Вычисление температуры смеси

#include <stdio.h>

#define SUCCESS 0

#define UNSUCCESS 1

int main(void)
{
    //Ввод данных
    float t1, t2 ,m1, m2, t;

    printf("Write temperature and volume: ");

    if (scanf("%f %f", &t1, &m1) != 2 || m1 < 0)
    {
        printf("Input error");
        return UNSUCCESS;
    }

    printf("Write another temperature and volume: ");

    if (scanf("%f %f", &t2, &m2) != 2 || m2 < 0)
    {
        printf("Input error");
        return UNSUCCESS;
    }

    t = (m1 * t1 + m2 * t2) / (m1 + m2); //t - итоговая температура
    printf("temperature: %.2f", t);
    return SUCCESS;
}
