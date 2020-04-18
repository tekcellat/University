//Определяет вид треугольника по координатам вершин

#include <stdio.h>
#include <math.h>

#define SUCCESS 0

#define UNSUCCESS 1

//Принимает длины сторон, печатает вид треугольника
int print_type(float l1, float l2, float l3)
{
    float cos_max_angle; //косинус максимального угла

    //сделаем l1 наибольшей стороной
    if (l2 > l1 && l2 > l3) //если l2 - наибольшая сторона
    {
        float temp = l1;
        l1 = l2;
        l2 = temp;
    }

    else if (l3 > l1 && l3 > l2) //если l3 - наибольшая сторона
    {
        float temp = l1;
        l1 = l3;
        l3 = temp;
    }

    cos_max_angle = (l3 * l3 + l2 * l2 - l1 * l1) / 2 / l2 / l3;

    //Выводим необходимое сообщение
    if (l1 >= l2 + l3) //неравенство треугольника
        printf("The triangle doesn't exist");
    else if (cos_max_angle > 10e-7)
        printf("Acute-angled");
    else if (cos_max_angle < -10e-7)
        printf("Obtuse");
    else
        printf("Rectangular");

    return SUCCESS;
}

//Считывает два числа типа float
int read_2_numbers(float *const x, float *const y)
{
    if (scanf("%f %f", x, y) != 2)
    {
        printf("Input error");
        return UNSUCCESS;
    }
    else
        return SUCCESS;
}

int main(void)
{
    float x1, x2, x3, y1, y2, y3; //координаты вершин треугольника
    float l1, l2, l3; //длины сторон треугольника

    //Считываем данные
    printf("Write the first coordinates: ");

    if (read_2_numbers(&x1, &y1) == UNSUCCESS)
            return UNSUCCESS;

    printf("Write the second coordinates: ");

    if (read_2_numbers(&x2, &y2) == UNSUCCESS)
            return UNSUCCESS;

    printf("Write the third coordinates: ");

    if (read_2_numbers(&x3, &y3) == UNSUCCESS)
            return UNSUCCESS;

    //вычисляем длины сторон
    l1 = sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2));
    l2 = sqrt(pow(x3 - x1, 2) + pow(y3 - y1, 2));
    l3 = sqrt(pow(x3 - x2, 2) + pow(y3 - y2, 2));

    if (print_type(l1, l2, l3) == UNSUCCESS)
        return UNSUCCESS;

    return SUCCESS;
}
