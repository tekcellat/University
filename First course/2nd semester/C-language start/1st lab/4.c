//Вычисление этажа и подъезда по номеру квартиры

#include <stdio.h>
#include <conio.h>

int main(void)
{
	//Ввод данных
	int apt,floor,entr; //apt - квартира, floor - этаж, entr - подъезд
	printf("Apartments: ");
	scanf("%d",&apt);
	
	entr = (apt - 1)/36 + 1; 
	floor = ((apt - 1)%36)/4 + 1;
	printf("Entrance %d, floor %d",entr,floor);
	getch();
	return 0;
}