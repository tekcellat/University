//Вычисление этажа и подъезда по номеру квартиры

#include <stdio.h>

#define NUM_FLOORS 9 //количество этажей

#define NUM_FLATS_FLOOR 4 //количество квартир на этаже

#define SUCCESS 0

#define UNSUCCESS 1

int main(void)
{
    //Ввод данных
    int apt, floor, entr; //apt - квартира, floor - этаж, entr - подъезд

    printf("Apartments: ");

    if (scanf("%d", &apt) != 1 || apt <= 0)
    {
        printf("Input error");
        return UNSUCCESS;
    }

    entr = (apt - 1) / (NUM_FLATS_FLOOR * NUM_FLOORS) + 1;
    floor = ((apt - 1) % (NUM_FLATS_FLOOR * NUM_FLOORS)) / NUM_FLATS_FLOOR + 1;
    printf("Entrance %d, floor %d", entr, floor);

    return SUCCESS;
}
