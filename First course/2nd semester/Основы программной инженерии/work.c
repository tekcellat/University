#include "stdio.h"
#include "conio.h"
#include "math.h"

int size_n(int n);          //размер массива
int array(int l, int n);   //массив 

int main()
{
	int n = size_n(10000);
	int arr_even[n], arr_odd[n],k = 0,l = 0;
	for(int i = 0; i <= n; i++)
	{
		int a = array(i,n);
		printf("%d ",a);
		if (a%2 == 0)
		{
			arr_even[k] = a; // массив с чёт числами 
			k++;
		}
		if (a%2 !=0)
		{
			arr_odd[l] = a;// массив с нечёт числами 
			l++;
		}
	}
	for(int i=1;i<k;i++)
	{
		for(int j=0;j<i;j++)
			if (arr_even[j] > arr_even[i])
			{
				int p = arr_even[i];
				arr_even[i] = arr_even[j];
				arr_even[j] = p;
			}
	}
	
	for(int i=1;i<l;i++)
	{
		for(int j=0;j<i;j++)
			if (arr_odd[j] < arr_odd[i])
			{
				int p = arr_odd[i];
				arr_odd[i] = arr_odd[j];
				arr_odd[j] = p;
			}
	}
	printf("\n");
	for(int j = 0; j < k; j++)
		printf("%d ",arr_even[j]);
	for(int j = 0; j < l; j++)
		printf("%d ",arr_odd[j]);
	getch();
	return 0;
}
int size_n(int n)
{
	FILE *file;	 
	file = fopen ("in.txt","r");
	int x[n], i = 0;
	while(1)
	{
		fscanf(file,"%d",x+i);
		if (feof(file))
			break;
		i++;
	}
	fclose(file);
	return i;
}
int array(int l, int n)
{
	FILE *file;	 
	file = fopen ("in.txt","r");
	int x[n], i = 0;
	while(1)
	{
		fscanf(file,"%d",x+i);
		if (feof(file))
			break;
		i++;
	}
	fclose(file);
	return x[l];
}