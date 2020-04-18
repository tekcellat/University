//Вычисление температуры смеси 

#include <stdio.h>
#include <conio.h>

int main(void)
{
	//Ввод данных
	float t1,t2,m1,m2,t;
	printf("Write temperature and volume: ");
	scanf("%f %f",&t1,&m1);
	printf("Write another temperature and volume: ");
	scanf("%f %f",&t2,&m2);
	if (t1 == 0 && t2 == 0 || m1 == 0 && m2 == 0)
	{
     printf("temprature is :0");
	}
	else
	{
	t = (m1*t1 + m2*t2)/(m1 + m2); //t - итоговая температура
	printf("temperature: %f",t);
	}
	getch();
}
