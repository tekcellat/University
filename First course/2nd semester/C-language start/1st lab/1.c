//Площади трапеции по основаниям и углу

#include "stdio.h"
#include "conio.h"
#include "math.h"

#define HEIGHT(a,b,angle) fabs((a-b)*tan(angle)/2) //Высота трапеции

int main(void)
{
	//Ввод данных
	float a,b,angle,S;
	printf("Write the length the first base: ");
	scanf("%f",&a);
	printf("Write the length of another base: ");
	scanf("%f",&b);
	printf("Write the angle in radians: ");
	scanf("%f",&angle);
	
	
	S = HEIGHT(a,b,angle)*(a+b)/2; 
	printf("S: %f",S);
	getch();
	return 0;
}