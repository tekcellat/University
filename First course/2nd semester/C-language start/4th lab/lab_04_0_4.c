#include<stdio.h>
int main() 
{
    int a[50], n, i, j, temp = 0;
    printf("Enter how many numbers you want:");
    scanf("%d", &n);
    if(n == 0 || n == 1)
    {
        printf("Not right arrive");
    }
    else
    {
        printf("Enter the %d elements:", n);
        for (i = 0; i < n; i++)
        {
            scanf("%d", &a[i]);
        }

        printf("The given array is:\n");
        for (i = 0; i < n; i++)
        {
            printf("%d ", a[i]);
        }
        for (i = 0; i < n; i++)
        {
            for (j = i + 1; j < n; j++)
            {
                if (a[i] > a[j])
                {
                    temp = a[i];
                    a[i] = a[j];
                    a[j] = temp;
                }
            }
        }
            
            printf("\nThe sorted array using Buble sort is:\n");
        for (i = 0; i < n; i++)
        {
            printf("%d ", a[i]);
        }
        return 0;
    }
}