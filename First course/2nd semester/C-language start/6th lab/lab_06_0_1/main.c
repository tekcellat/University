// Многофайловый проект без заголовочных файлов

#include <stdio.h>

#define SUCCESS 0
#define WRONG_PARAMETERS -1
#define FILE_ERROR -2
#define NMAX 100

int read_array(FILE *f, int *a, int *const n);
int count(const int *pbegin, const int *pend, int *const max);

int main(int argc, char **argv)
{
    FILE *f;
    int a[NMAX], *pend, n = 0; //pend - указатель на последний элемент массива a
    int max;
    int status;

    //Проверка количества параметров командной строки
    if (argc != 2)
    {
        fprintf(stderr, "Wrong parameters\nmain.exe <file-name>\n");

        return WRONG_PARAMETERS;
    }

    //Проверка и открытие файла
    f = fopen(argv[1], "r");
    if (f == NULL)
    {
        perror("Error opening file");

        return FILE_ERROR;
    }

    status = read_array(f, a, &n);

    pend = a + n - 1;

    if (status == SUCCESS) //нахождение и вывод искомой величины
    {
        count(a, pend, &max);
        printf("%d", max);
    }

    // Закрытие файла
    if (fclose(f) != 0)
    {
        perror("Error closing file");

        return FILE_ERROR;
    }

    return status;
}

