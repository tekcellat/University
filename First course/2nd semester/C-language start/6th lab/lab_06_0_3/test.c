//Модульные тесты функций read_array() и count()
#include <stdio.h>
#include "count.h"
#include "read_array.h"

#define SUCCESS 0
#define WRONG_PARAMETERS -1
#define FILE_ERROR -2
#define EMPTY_FILE -3
#define INPUT_ERROR -4

void test_read_array(void)
{
    FILE *f;
    int a[100], n;
    int status, num_tests = 0;

    printf("\nread_array():\n\n");

    // Обычные данные
    printf("test 1: ");
    f = fopen("tests/in_1.txt", "r");
    status = read_array(f, a, &n);

    if (status == SUCCESS && n == 6 && a[0] == 5 && a[1] == 2 && a[2] == 7 &&
        a[3] == 4 && a[4] == 0 && a[5] == 3)
    {
        num_tests += 1;
        printf("\nSUCCESS\n\n");
    }
    else
    {
        printf("\nexpected: n = 6, a = {5, 2, 7, 4, 0, 3}");
        printf(", return = 0\nactual: n = %d, a = {%d, %d, %d, %d, %d, %d}, ",
           n, a[0], a[1], a[2], a[3], a[4], a[5]);
        printf("return = %d\nUNSUCCESS\n\n", status);
    }

    // Обычные данные
    printf("test 2: ");
    f = fopen("tests/in_2.txt", "r");
    status = read_array(f, a, &n);

    if (status == SUCCESS && n == 5 && a[0] == 5 && a[1] == 7 && a[2] == 8 &&
        a[3] == 5 && a[4] == 1)
    {
        num_tests += 1;
        printf("\nSUCCESS\n\n");
    }
    else
    {
        printf("\nexpected: n = 5, a = {5, 7, 8, 5, 1}");
        printf(", return = 0\nactual: n = %d, a = {%d, %d, %d, %d, %d}, ",
           n, a[0], a[1], a[2], a[3], a[4]);
        printf("return = %d\nUNSUCCESS\n\n", status);
    }

    // Пустой файл
    printf("test 3: ");
    f = fopen("tests/in_3.txt", "r");
    status = read_array(f, a, &n);

    if (status == EMPTY_FILE)
    {
        num_tests += 1;
        printf("\nSUCCESS\n\n");
    }
    else
    {
        printf("\nexpected: return = -3\nactual:");
        printf(" return = %d\nUNSUCCESS\n\n", status);
    }

    // Некорректный ввод
    printf("test 4: ");
    f = fopen("tests/in_4.txt", "r");
    status = read_array(f, a, &n);

    if (status == INPUT_ERROR)
    {
        num_tests += 1;
        printf("\nSUCCESS\n\n");
    }
    else
    {
        printf("\nexpected: return = -4\nactual:");
        printf(" return = %d\nUNSUCCESS\n\n", status);
    }

    // Больше ста чисел
    printf("test 5: ");
    f = fopen("tests/in_5.txt", "r");
    status = read_array(f, a, &n);

    if (n == 100)
    {
        num_tests += 1;
        printf("SUCCESS\n\n");
    }
    else
    {
        printf("\nexpected: n == 100\nactual:");
        printf(" n = %d\nUNSUCCESS\n\n", n);
    }

    printf("Total: %d/5\n", num_tests);
}

void test_count(void)
{
    int a[6] = {5, 2, 7, 4, 0, 3};
    int max;
    int status, num_tests = 0;

    printf("\ncount():\n\n");

    // Обычные данные
    printf("test 1: ");
    status = count(a, a + 5, &max);

    if (status == SUCCESS && max == 11)
    {
        num_tests += 1;
        printf("\nSUCCESS\n\n");
    }
    else
    {
        printf("\nexpected: max = 11, return = 0\n");
        printf("actual: max = %d, return = %d\nUNSUCCESS\n\n", max, status);
    }

    // Нечетное количество элементов
    a[0] = 5;
    a[1] = 7;
    a[2] = 8;
    a[3] = 5;
    a[4] = 1;

    printf("test 2: ");
    status = count(a, a + 4, &max);

    if (status == SUCCESS && max == 12)
    {
        num_tests += 1;
        printf("\nSUCCESS\n\n");
    }
    else
    {
        printf("\nexpected: max = 12, return = 0\n");
        printf("actual: max = %d, return = %d\nUNSUCCESS\n\n", max, status);
    }

    // Неверные параметры
    printf("test 3: ");
    status = count(a, a - 1, &max);

    if (status == WRONG_PARAMETERS)
    {
        num_tests += 1;
        printf("\nSUCCESS\n\n");
    }
    else
    {
        printf("\nexpected: return = -1\n");
        printf("actual: return = %d\nUNSUCCESS\n\n", status);
    }

    printf("Total: %d/3\n", num_tests);
}

int main(void)
{
    test_read_array();
    test_count();

    return 0;
}
