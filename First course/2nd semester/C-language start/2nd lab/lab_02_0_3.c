//Вычисляет точное и приближенное значение функции f(x) = e^x с точностью eps

#include <stdio.h>
#include <math.h>

#define SUCCESS 0

#define UNSUCCESS 1

//Возвращает s - значение ряда в точке x с точностью eps
float series_value(float x, float eps)
{
    float s = 0;
    float last_term = 1; //последний посчитанный элемент ряда

    for (int i = 1; last_term > eps; i++)
    {
        s += last_term;
        last_term *= x / i; //вычисляем last_term - (i+1)-ый элемент
    }

    return s;
}

//Считывает число типа float
int read_number(float *const p)
{
    if (scanf("%f", p) != 1)
    {
        printf("Input error");
        return UNSUCCESS;
    }
    else
        return SUCCESS;
}

int main(void)
{
    float x;
    float eps;
    float s, f; //s - приближенное, f - точное значения функции

    //Считываем данные
    printf("x: ");

    if (read_number(&x) == UNSUCCESS)
        return UNSUCCESS;

    printf("eps: ");

    if (read_number(&eps) == UNSUCCESS)
        return UNSUCCESS;

    s = series_value(x, eps);
    f = exp(x);

    //Вывод результатов
    printf("s(x) = %f\n", s);
    printf("f(x) = %f\n", f);
    printf("|f(x) - s(x)| = %f\n", fabs(f - s));
    printf("|(f(x) - s(x))/f(x)| = %.3f %c", fabs((f - s) / f) * 100, '%');

    return SUCCESS;
}
