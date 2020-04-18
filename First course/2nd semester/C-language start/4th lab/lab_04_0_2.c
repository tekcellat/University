#include <stdio.h>
void main()
{
    int n, i, res, m, arr[50], sum = 0;
    int size = 0, b[50];
    printf("How many number you want to enter ?\n");
    res=scanf("%d", &n);
    if( n == 0 || n ==1 || n>10 || (res!=1) )
        printf("Not right size of array");
    else
    {
        printf("Enter %d Numbers :", n);
        for (i = 0; i < n; i++)
        {
            m=scanf("%d", &arr[i]);
            if(m!=1)
                printf("Error");
            else
            { 
                sum = sum + arr[i];
            }
            int average = sum / n;
            for (i = 0; i < n; i++)
                if (arr[i] > average)
                {
                    b[size] = arr[i];
                    size++;
                }
            printf("New array: ");
            for (i = 0; i < size; i++)
                printf("%d ", b[i]);
        }
    }
}