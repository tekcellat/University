//Площади трапеции по основаниям и углу

#include <stdio.h>
#include <math.h>

#define SUCCESS 0

#define UNSUCCESS 1

int main(void)
{
    //Ввод данных
    float a, b, angle, s;

    printf("Write the length the first base: ");

    if (scanf("%f", &a) != 1 || a <= 0)
    {
        printf("\nInput error");
        return UNSUCCESS;
    }

    printf("Write the length of another base: ");
    if (scanf("%f", &b) != 1 || b <= 0)
    {
        printf("\nInput error");
        return UNSUCCESS;
    }

    printf("Write the angle in radians: ");
    if (scanf("%f", &angle) != 1 || angle <= 0)
    {
        printf("\nInput error");
        return UNSUCCESS;
    }

    s = fabs((a - b) * tan(angle) / 2) * (a + b) / 2;
    printf("S: %f", s);
    return SUCCESS;
}
