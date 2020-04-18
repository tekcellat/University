/* Создает и заполняет двоичный файл не более чем 25-ю случайными
 * положительными целыми числами, не превышающими 1000, выводит числа из файла
 * на экран, упорядочивает в файле числа по возрастанию методом вставок */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <errno.h>

#define SUCCESS 0
#define UNSUCCESS -1
#define MAXFILESIZE 25
#define MAXNUMSIZE 1000
#define FILENAME "data.bin"

// Возвращает целочисленное значение из позиции pos бинарного файла f
int get_number_by_pos(FILE *f, const int pos)
{
    int temp;

    fseek(f, pos * sizeof(int), SEEK_SET);
    fread(&temp, sizeof(int), 1, f);

    return temp;
}

// Вставляет целочисленное значение num на позицию pos в бинарный файл f
int put_number_by_pos(FILE *f, const int num, const int pos)
{
    fseek(f, pos * sizeof(int), SEEK_SET);
    if (fwrite(&num, sizeof(int), 1, f) != 1)
        return UNSUCCESS;

    return SUCCESS;
}

/* Заполняет бинарный файл f случайными числами,
 * записывает в N количество чисел */
int create_random_file(FILE *f, int *const N)
{
    int temp;

    rewind(f);
    srand(time(NULL));

    *N = rand() % MAXFILESIZE + 1;

    for (int i = 0; i < *N; i++)
    {
        temp = rand() % MAXNUMSIZE + 1;
        if (fwrite(&temp, sizeof(int), 1, f) != 1)
            return UNSUCCESS;
    }

    return SUCCESS;
}

// Печатает числа бинарного файла f
int print_file(FILE *f)
{
    int temp;

    rewind(f);

    while (fread(&temp, sizeof(int), 1, f))
        printf("%d ", temp);

    printf("\n");

    return SUCCESS;
}

// Сортирует методом вставок бинарный файл f размерном в N чисел
int sort_file(FILE *f, const int N)
{
    for (int valuej, valuei, j, i = 1; i < N; i++)
    {
        j = i - 1;

        valuei = get_number_by_pos(f, i);
        valuej = get_number_by_pos(f, j);

        // Сдвиг i-ого числа влево
        while (j >= 0 && valuej > valuei)
        {
            put_number_by_pos(f, valuej, j + 1);
            j--;
            valuej = get_number_by_pos(f, j);
        }

        put_number_by_pos(f, valuei, j + 1);
    }

    return SUCCESS;
}

int close_file(FILE *f)
{
    if (fclose(f) != 0)
    {
        fprintf(stderr, "Error closing file: %s", strerror(errno));

        return UNSUCCESS;
    }

    return SUCCESS;
}

int main(void)
{
    FILE *f;
    int N; //количество чисел

    setbuf(stdout, NULL); //дебуферизация

    // Создание и заполнение файла
    f = fopen(FILENAME, "wb");
    create_random_file(f, &N);

    if (close_file(f) != SUCCESS)
        return UNSUCCESS;

    f = fopen(FILENAME, "rb+");

    // Печать неотсортированного файла
    printf("Unsorted: ");
    print_file(f);

    sort_file(f, N);

    // Печать отсортированного файла
    printf("Sorted: ");
    print_file(f);

    if (close_file(f) != SUCCESS)
        return UNSUCCESS;

    return SUCCESS;
}
