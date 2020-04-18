#include <stdio.h>

int solve(int t);

int main()
{
	int t;
	printf("Input num\n");
	scanf("%d",&t);
	printf("%d = ",t);

	solve(t);
	return 0;
}

int solve(int t)
{
	int i=2;
	if(t==1 || t==0 || t==-1)
		printf("Invalid input");
	else
	{
		while(i <= t)
		{
			if(t%i == 0)
			{
				printf("%d",i);
				t= t/i;
				if(t>1)
					printf("*");
			}
			else
				i=i+1;	
		}
	}
	return 0;
}